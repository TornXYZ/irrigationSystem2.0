from pumpControl import pump
import registerControl
import adcControl
import fileManager
import exceptions
import threading

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


class flowerpotManager(threading.Thread):
    "This class holds all flowerpots and provides handling functions."

    def __init__(self, config) -> None:
        super().__init__()
        self.stop_execution = False
        self.data_available = False
        self.output_path = config.config['PATHS']['DATA_OUTPUT_PATH']
        self.pot_dump_path = config.config['PATHS']['POT_DUMP_PATH']
        self.saturation_sleep_time = int(config.config['PARAMS']['SAMPLE_SATURATION_SLEEP_IN_MS']) / 1000
        self.sample_rate = int(config.config['PARAMS']['SAMPLE_RATE_IN_MS']) / 1000
        self.pump = pump(config.pump)
        self.sensor_register = registerControl.register(config.ser, config.sclk, config.rclk_sensor)
        self.valve_register = registerControl.register(config.ser, config.sclk, config.rclk_valve)
        self.adc = adcControl.adc()
        self.file_manager = fileManager.fileManager()
        self.last_timestamp = int

        self.highest_occupied_slot = 0
        self.pot_collection = []
        self.initialize_pot_collection(self.pot_dump_path)
        return


    def initialize_pot_collection(self, path) -> None:
        print(f"Initialize after restart.")
        parsed_pots = self.file_manager.read_json(path)

        for parsed_pot in parsed_pots:
            new_pot = flowerpot(parsed_pot['slot'], parsed_pot['name'])

            new_pot.is_active = parsed_pot['is_active']
            new_pot.expected_moisture = parsed_pot['expected_moisture']

            self.add_pot(new_pot)

            if self.highest_occupied_slot < new_pot.slot:
                self.highest_occupied_slot = new_pot.slot

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
        for pot in self.pot_collection:
            if pot.slot == new_pot.slot:
                print(f"Slot {new_pot.slot} already occupied! No pot has been added.")
                raise exceptions.PotDoubletteError
        
        self.pot_collection.append(new_pot)
        if self.highest_occupied_slot < new_pot.slot:
            self.highest_occupied_slot = new_pot.slot

        self.pot_collection.sort(key=lambda pot: pot.slot)

        self.retrieve_single_data(new_pot)
        self.dump_pot_collection()
        return


    def remove_pot(self, slot: int) -> None:
        for pot in self.pot_collection:
            if pot.slot == slot:
                self.pot_collection.remove(pot)
                self.dump_pot_collection()
                return
        print(f"Pot at slot {slot} is not existing! No pot has been deleted.")
        raise exceptions.PotNotExistingError


    def retrieve_single_data(self, pot: flowerpot) -> None:
        self.sensor_register.set_single_bit(pot.slot)
        time.sleep(self.saturation_sleep_time) # sleep to wait for sensor saturation
        adc_channel_output = self.adc.retrieve_data()
        pot.set_actual_moisture(adc_channel_output.value)

        self.sensor_register.clear()
        self.new_data_available = True
        return
            

    def retrieve_all_data(self) -> None:
        self.last_timestamp = datetime.now()
        for pot in self.pot_collection:
            self.retrieve_single_data(pot)

        self.file_manager.write_data_to_file(self.output_path, self.last_timestamp, self.pot_collection)
        self.data_available = True
        return


    def run(self) -> None:
        while(not self.stop_execution):
            time.sleep(self.sample_rate)
            self.retrieve_all_data()