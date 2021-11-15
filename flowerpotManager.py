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
        self.isActive = True
        self.actualMoisture = measurement
        self.expectedMoisture = 0
        return


    def needsWater(self) -> bool:
        if(self.actualMoisture <= self.expectedMoisture):
            return True
        else:
            return False


class flowerpotManager:
    "This class holds all flowerpots and provides handling functions."

    def __init__(self) -> None:
        self.allFlowerpots: List[flowerpot] = []
        self.config = configurationManager.configuration('config.ini')
        self.pump = pump(self.config.pump)
        self.sensorRegister = registerControl.register(self.config.ser, self.config.sClk, self.config.rClkSensor)
        self.valveRegister = registerControl.register(self.config.ser, self.config.sClk, self.config.rClkValve)
        self.adc = adcControl.adc()
        return


    def addFlowerpot(self, slot: int, name: str) -> None:
        pot = flowerpot(slot, name)
        self.allFlowerpots.append(pot)
        return


    #def removeFlowerpot(self, flowerpotID):


    def retrieveSingleData(self, pot: flowerpot, currentTime: datetime) -> None:
        self.sensorRegister.setSingleBit(pot.slot)
        adcChannelOutput = self.adc.retrieveData()
        pot.actualMoisture.timestamp = currentTime
        pot.actualMoisture.voltage = adcChannelOutput.voltage
        pot.actualMoisture.value = adcChannelOutput.value

        self.sensorRegister.clear()
        return


    def retrieveAllData(self) -> None:
        currentTime = datetime.now()

        for pot in self.allFlowerpots:
            if (pot.isActive):
                self.retrieveSingleData(pot, currentTime)
        return
        
    # def writeDataToFile


class measurement:
    "Contains a measurement with value and timestamp"

    def __init__(self, timestamp: datetime, voltage: int, value: float) -> None:
        self.value = value
        self.voltage = voltage
        self.timestamp = timestamp
        return