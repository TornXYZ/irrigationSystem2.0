from pumpControl import pump
import registerControl
import adcControl
import fileManager
import exceptions

from datetime import datetime
import time

class flowerpot:
    "Class which represents a flowerpot."

    def __init__(self, slot: int, name: str) -> None:
        self.slot = slot
        self.name = name
        self.is_active = True
        self.actual_moisture = 0
        self.expected_moisture = 0
        return


    def set_actual_moisture(self, actual_moisture) -> None:
        self.actual_moisture = actual_moisture
        return

    def set_expected_moisture(self, moisture: int) -> None:
        self.expected_moisture = moisture
        return

    def activate(self) -> None:
        self.is_active = True
        return

    def deactivate(self) -> None:
        self.is_active = False
        return


    def needs_water(self) -> bool:
        if(self.actual_moisture <= self.expected_moisture):
            return True
        else:
            return False


class flowerpotManager:
    "This class holds all flowerpots and provides handling functions."

    def __init__(self, config) -> None:
        self.output_path = config.config['PATHS']['DATA_OUTPUT_PATH']
        self.pot_dump_path = config.config['PATHS']['POT_DUMP_PATH']
        self.saturation_sleep_time = int(config.config['PARAMS']['SAMPLE_SATURATION_SLEEP_IN_MS']) / 1000
        self.pump = pump(config.pump)
        self.sensor_register = registerControl.register(config.ser, config.sclk, config.rclk_sensor)
        self.valve_register = registerControl.register(config.ser, config.sclk, config.rclk_valve)
        self.adc = adcControl.adc()
        self.file_manager = fileManager.fileManager()
        self.last_timestamp = int

        self.pot_collection = []
        self.initialize_pot_collection(self.pot_dump_path)
        return


    def initialize_pot_collection(self, path) -> None:
        print(f"Initialize after restart.")
        parsed_pots = self.file_manager.read_json(path)

        for parsed_pot in parsed_pots:
            name = parsed_pot['name']
            slot = parsed_pot['slot']
            new_pot = flowerpot(slot, name)

            new_pot.is_active = parsed_pot['is_active']
            new_pot.expected_moisture = parsed_pot['expected_moisture']

            self.add_pot(new_pot)

        print(f"Initialization complete.")
        return


    def clear_pot_collection(self) -> None:
        self.pot_collection.clear()
        self.dump_pot_collection()
        return


    def dump_pot_collection(self) -> None:
        self.file_manager.dump_data_to_json(self.pot_collection, self.pot_dump_path)
        return


    def add_pot(self, new_pot: flowerpot) -> None:
        def fill_slot_gap_with_dummy_pots(start_index, end_index):
            def add_dummy_pot(slot):
                new_dummy_pot = flowerpot(slot, "<empty>")
                self.pot_collection.append(new_dummy_pot)
                print(f"Dummy pot added to collection at slot {slot}")
                return

            index = start_index
            while index <= end_index:
                add_dummy_pot(index)
                index += 1
            return

        def update_pot(new_pot):
            if self.pot_collection[new_pot.slot].name != "<empty>":
                print(f"Slot {new_pot.slot} already occupied! Pot has not been added.")
                raise exceptions.PotDoubletteError
            
            self.pot_collection[new_pot.slot] = new_pot
            print(f"Dummy pot at slot {new_pot.slot} overwritten!")
            print(f"Pot \"{new_pot.name}\" added to collection at slot {new_pot.slot}.")
            return

            
        pot_collection_length = len(self.pot_collection)

        if pot_collection_length == new_pot.slot:
            self.pot_collection.append(new_pot)
            print(f"Pot \"{new_pot.name}\" added to collection at slot {new_pot.slot}.")
        elif pot_collection_length < new_pot.slot:
            fill_slot_gap_with_dummy_pots(pot_collection_length, new_pot.slot - 1)
            self.pot_collection.append(new_pot)
            print(f"Pot \"{new_pot.name}\" added to collection at slot {new_pot.slot}.")
        elif pot_collection_length > new_pot.slot:
            update_pot(new_pot)

        self.retrieve_single_data(new_pot)
        
        self.dump_pot_collection()
        return


    def remove_pot(self, slot: int) -> None:
        def remove_last_dummy_pots():
            last_pot_is_dummy = True
            while last_pot_is_dummy:
                if self.pot_collection[-1].name == "<empty>":
                    print(f"Dummy pot at slot {self.pot_collection[-1].slot} removed.")
                    del self.pot_collection[-1]
                else:
                    last_pot_is_dummy = False
            return

        def overwrite_slot_with_dummy_pot(slot):
                new_dummy_pot = flowerpot(slot, "<empty>")
                self.pot_collection[slot] = new_dummy_pot
                print(f"Pot at slot {slot} removed and replaced by dummy pot.")
                return

        pot_collection_length = len(self.pot_collection)

        if pot_collection_length - 1 == slot:
            print(f"Pot \"{self.pot_collection[slot].name}\" removed.")
            del self.pot_collection[slot]
            remove_last_dummy_pots()
        elif pot_collection_length - 1 < slot:
            print(f"No pot listed for slot {slot}")
        elif pot_collection_length - 1 > slot:
            overwrite_slot_with_dummy_pot(slot)
        
        self.dump_pot_collection()
        return


    def retrieve_single_data(self, pot: flowerpot) -> None:
        self.sensor_register.set_single_bit(pot.slot)
        time.sleep(self.saturation_sleep_time) # sleep to wait for sensor saturation
        adc_channel_output = self.adc.retrieve_data()
        pot.set_actual_moisture(adc_channel_output.value)

        self.sensor_register.clear()
        return
            

    def retrieve_all_data(self) -> None:
        self.last_timestamp = datetime.now()
        [self.retrieve_single_data(pot) for pot in self.pot_collection if pot.is_active and pot.name != "<empty>"]
        self.file_manager.write_data_to_file(self.output_path, self.last_timestamp, self.pot_collection)
        return