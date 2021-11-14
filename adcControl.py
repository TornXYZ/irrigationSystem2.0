import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class adc:
    "This class controls the ADC."

    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS.ADS1015(self.i2c)
        self.chan = AnalogIn(self.ads, ADS.P0)

    def retrieveData(self):
        print(self.chan.value, self.chan.voltage)
        return self.chan
