import RPi.GPIO as GPIO

class pump:
    "This class controls the pump."

    def __init__(self, pumpPin):
        self.pumpPin = pumpPin
        self.pumpIsRunning = False

        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.pumpPin, GPIO.OUT)

    def start(self):
        GPIO.output(self.pumpPin, GPIO.HIGH)
        self.pumpIsRunning = True

    def stop(self):
        GPIO.output(self.pumpPin, GPIO.LOW)
        self.pumpIsRunning = False