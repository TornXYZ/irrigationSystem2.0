from pumpControl import pump
import registerControl
import configurationManager
import adcControl
from datetime import datetime
import numpy as np
from typing import List

class flowerpot:
    "Class which represents a flowerpot."

    def __init__(self, slot: int, name: str) -> None:
        self.slot = slot
        self.name = name
        self.is_active = True
        self.actual_moisture = measurement
        self.expected_moisture = 0
        return


    def needs_water(self) -> bool:
        if(self.actual_moisture <= self.expected_moisture):
            return True
        else:
            return False


class flowerpotManager:
    "This class holds all flowerpots and provides handling functions."

    def __init__(self) -> None:
        self.all_flowerpots: List[flowerpot] = []
        self.config = configurationManager.configuration('config.ini')
        self.pump = pump(self.config.pump)
        self.sensor_register = registerControl.register(self.config.ser, self.config.sclk, self.config.rclk_sensor)
        self.valve_register = registerControl.register(self.config.ser, self.config.sclk, self.config.rclk_valve)
        self.adc = adcControl.adc()
        return


    def add_flowerpot(self, slot: int, name: str) -> None:
        pot = flowerpot(slot, name)
        self.all_flowerpots.append(pot)
        return


    #def removeFlowerpot(self, flowerpotID):


    def retrieve_single_data(self, pot: flowerpot, current_time: datetime) -> None:
        self.sensor_register.set_single_it(pot.slot)
        adc_channel_output = self.adc.retrieve_data()
        pot.actual_moisture.timestamp = current_time
        pot.actual_moisture.voltage = adc_channel_output.voltage
        pot.actual_moisture.value = adc_channel_output.value

        self.sensor_register.clear()
        return


    def retrieveAllData(self) -> None:
        current_time = datetime.now()

        for pot in self.all_flowerpots:
            if (pot.is_active):
                self.retrieve_single_data(pot, current_time)
        return
        
    # def writeDataToFile


class measurement:
    "Contains a measurement with value and timestamp"

    def __init__(self, timestamp: datetime, voltage: int, value: float) -> None:
        self.value = value
        self.voltage = voltage
        self.timestamp = timestamp
        return