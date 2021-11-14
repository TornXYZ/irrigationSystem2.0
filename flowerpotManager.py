from pumpControl import pump
import registerControl
import configurationManager
import adcControl
from datetime import datetime
import numpy as np

class flowerpotManager:
    "This class holds all flowerpots and provides handling functions."

    def __init__(self):
        self.allFlowerpots = []
        self.pump = pump
        self.config = configurationManager.configuration('config.ini')
        self.sensorRegister = registerControl.register(self.config.ser, self.config.sClk, self.config.rClkSensor)
        self.valveRegister = registerControl.register(self.config.ser, self.config.sClk, self.config.rClkValve)
        self.adc = adcControl.adc()

    def addFlowerpot(self, slot, name):
        pot = flowerpot(slot, name)
        self.allFlowerpots.append(pot)

    #def removeFlowerpot(self, flowerpotID):

    def retrieveSingleData(self, pot, currentTime):
        self.sensorRegister.setSingleBit(pot.slot)
        adcChannelOutput = self.adc.retrieveData()
        pot.actualMoisture.timestamp = currentTime
        pot.actualMoisture.voltage = adcChannelOutput.voltage
        pot.actualMoisture.value = adcChannelOutput.value

        self.sensorRegister.clear()

    def retrieveAllData(self):
        currentTime = datetime.now()

        for pot in self.allFlowerpots:
            if (pot.isActive):
                self.retrieveSingleData(pot, currentTime)
        
    # def writeDataToFile

class measurement:
    "Defines a measurement with value and timestamp"

    def __init__(self, timestamp, voltage, value):
        self.value = value
        self.voltage = voltage
        self.timestamp = timestamp


class flowerpot:
    "Class which represents a flowerpot."

    def __init__(self, slot, name):
        self.slot = slot
        self.name = name
        self.isActive = True
        self.actualMoisture = measurement
        self.expectedMoisture = 0

    def needsWater(self):
        if(self.actualMoisture <= self.expectedMoisture):
            return True
        else:
            return False

