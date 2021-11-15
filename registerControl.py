import RPi.GPIO as GPIO
from bitarray import bitarray
import time

class register:
    "This class controls shift registers."

    def __init__(self, serial_data_pin: int, serial_clock_pin: int, register_clock_pin: int) -> None:
        self.serial_data_din = serial_data_pin
        self.serial_clock_pin = serial_clock_pin
        self.register_clock_pin = register_clock_pin
        self.max_supported_pots = 16

        self.setup()
        return

    def setup(self) -> None:
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.serial_data_din, GPIO.OUT)
        GPIO.setup(self.serial_clock_pin, GPIO.OUT)
        GPIO.setup(self.register_clock_pin, GPIO.OUT)
        return


    def pulse(self, output_pin: int) -> None:
        GPIO.output(output_pin, GPIO.LOW)
        GPIO.output(output_pin, GPIO.HIGH)
        GPIO.output(output_pin, GPIO.LOW)
        return


    def clear(self) -> None:
        GPIO.output(self.serial_data_din, GPIO.LOW)

        for _ in range(self.max_supported_pots):
            self.pulse(self.serial_clock_pin)

        self.pulse(self.register_clock_pin)
        print("Register cleared!")
        return


    def setRegisterOutput(self, input_bitarray: bitarray) -> None:
        input_bitarray = input_bitarray[::-1]

        for bit in input_bitarray:
            if(bit == False):
                GPIO.output(self.serial_data_din, GPIO.LOW)
            else:
                GPIO.output(self.serial_data_din, GPIO.HIGH)

            self.pulse(self.serial_clock_pin)

        self.pulse(self.register_clock_pin)
        print("Register set to: " + str(input_bitarray))
        time.sleep(0.01) # sleep to wait for sensor saturation
        return

        
    def set_single_it(self, slot: int) -> None:
        array = bitarray(slot + 1)
        array.setall(0)
        array[slot] = 1

        self.setRegisterOutput(array)
        return