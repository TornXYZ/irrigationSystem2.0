import RPi.GPIO as GPIO
from bitarray import bitarray
import time

class register:
    "This class controls shift registers."

    def __init__(self, serialDataPin: int, serialClockPin: int, registerClockPin: int) -> None:
        self.serialDataPin = serialDataPin
        self.serialClockPin = serialClockPin
        self.registerClockPin = registerClockPin
        self.maxSupportedPots = 16

        self.setup()
        return

    def setup(self) -> None:
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.serialDataPin, GPIO.OUT)
        GPIO.setup(self.serialClockPin, GPIO.OUT)
        GPIO.setup(self.registerClockPin, GPIO.OUT)
        return


    def pulse(self, outputPin: int) -> None:
        GPIO.output(outputPin, GPIO.LOW)
        GPIO.output(outputPin, GPIO.HIGH)
        GPIO.output(outputPin, GPIO.LOW)
        return


    def clear(self) -> None:
        GPIO.output(self.serialDataPin, GPIO.LOW)

        for _ in range(self.maxSupportedPots):
            self.pulse(self.serialClockPin)

        self.pulse(self.registerClockPin)
        print("Register cleared!")
        return


    def setRegisterOutput(self, inputBitarray: bitarray) -> None:
        inputBitarray = inputBitarray[::-1]

        for bit in inputBitarray:
            if(bit == False):
                GPIO.output(self.serialDataPin, GPIO.LOW)
            else:
                GPIO.output(self.serialDataPin, GPIO.HIGH)

            self.pulse(self.serialClockPin)

        self.pulse(self.registerClockPin)
        print("Register set to: " + str(inputBitarray))
        time.sleep(0.01) # sleep to wait for sensor saturation
        return

        
    def setSingleBit(self, slot: int) -> None:
        array = bitarray(slot + 1)
        array.setall(0)
        array[slot] = 1

        self.setRegisterOutput(array)
        return