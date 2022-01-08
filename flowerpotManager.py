from pumpControl import pump
import registerControl
import configurationManager
import adcControl
import fileManager
from datetime import datetime

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


    def needs_water(self) -> bool:
        if(self.actual_moisture <= self.expected_moisture):
            return True
        else:
            return False


class flowerpotManager:
    "This class holds all flowerpots and provides handling functions."

    def __init__(self) -> None:
        self.all_flowerpots = []
        self.config = configurationManager.configuration('config.ini')
        self.pump = pump(self.config.pump)
        self.sensor_register = registerControl.register(self.config.ser, self.config.sclk, self.config.rclk_sensor)
        self.valve_register = registerControl.register(self.config.ser, self.config.sclk, self.config.rclk_valve)
        self.adc = adcControl.adc()
        self.file_manager = fileManager.fileManager()
        self.last_timestamp = int
        return


    def add_flowerpot(self, slot: int, name: str) -> flowerpot:
        # add check for overwriting slots
        pot = flowerpot(slot, name)
        self.all_flowerpots.append(pot)
        self.all_flowerpots.sort(key=lambda pot: pot.slot)
        return pot


    def remove_flowerpot(self, slot: int) -> None:
        def find_pot_by_slot():
            for pot in self.all_flowerpots:
                if pot.slot == slot:
                    return pot

        self.all_flowerpots.remove(find_pot_by_slot())


    def retrieve_single_data(self, pot: flowerpot) -> None:
        self.sensor_register.set_single_bit(pot.slot)
        adc_channel_output = self.adc.retrieve_data()
        pot.set_actual_moisture(measurement(adc_channel_output.voltage, adc_channel_output.value))

        self.sensor_register.clear()
        return
            

    def retrieve_all_data(self) -> None:
        self.last_timestamp = datetime.now()
        [self.retrieve_single_data(pot) for pot in self.all_flowerpots if pot.is_active]
        self.file_manager.write_data_to_file('example.csv', self.last_timestamp, self.all_flowerpots)
        return