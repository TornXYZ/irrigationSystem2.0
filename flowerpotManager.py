from pumpControl import pump
import registerControl
import adcControl
import fileManager
from datetime import datetime
import time

class measurement:
    "Contains a measurement with voltage and value"

    def __init__(self, voltage: int, value: float) -> None:
        self.value = value
        self.voltage = voltage
        return

class flowerpot:
    "Class which represents a flowerpot."

    def __init__(self, slot: int, name: str) -> None:
        self.slot = slot
        self.name = name
        self.is_active = True
        self.actual_moisture = measurement
        self.expected_moisture = 0
        return


    def set_actual_moisture(self, moisture: measurement) -> None:
        self.actual_moisture = moisture
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
        self.all_flowerpots = []
        self.output_path = config.config['PATHS']['DATA_OUTPUT_PATH']
        self.saturation_sleep_time = int(config.config['PARAMS']['SAMPLE_SATURATION_SLEEP_IN_MS']) / 1000
        self.pump = pump(config.pump)
        self.sensor_register = registerControl.register(config.ser, config.sclk, config.rclk_sensor)
        self.valve_register = registerControl.register(config.ser, config.sclk, config.rclk_valve)
        self.adc = adcControl.adc()
        self.file_manager = fileManager.fileManager()
        self.last_timestamp = int
        return


    def add_flowerpot(self, slot: int, name: str) -> flowerpot:
        
        for pot in self.all_flowerpots:
            if slot == pot.slot:
                print("Slot is already occupied! Pot has not been added.")
                return None
            elif name == pot.name:
                print("Pot name exists already!")

        new_pot = flowerpot(slot, name)
        self.all_flowerpots.append(new_pot)
        self.all_flowerpots.sort(key=lambda pot: pot.slot)
        return new_pot


    def remove_flowerpot(self, slot: int) -> None:
        def find_pot_by_slot():
            for pot in self.all_flowerpots:
                if pot.slot == slot:
                    return pot

        self.all_flowerpots.remove(find_pot_by_slot())


    def retrieve_single_data(self, pot: flowerpot) -> None:
        self.sensor_register.set_single_bit(pot.slot)
        time.sleep(self.saturation_sleep_time) # sleep to wait for sensor saturation
        adc_channel_output = self.adc.retrieve_data()
        pot.set_actual_moisture(measurement(adc_channel_output.voltage, adc_channel_output.value))

        self.sensor_register.clear()
        return
            

    def retrieve_all_data(self) -> None:
        self.last_timestamp = datetime.now()
        [self.retrieve_single_data(pot) for pot in self.all_flowerpots if pot.is_active]
        self.file_manager.write_data_to_file(self.output_path, self.last_timestamp, self.all_flowerpots)
        return