import RPi.GPIO as GPIO

class pump:
    "This class controls the pump."

    def __init__(self, pumpPin: int) -> None:
        self.pumpPin = pumpPin
        self.pumpIsRunning = False

        self.setup()
        return

    def setup(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pumpPin, GPIO.OUT)
        return

    def start(self) -> None:
        GPIO.output(self.pumpPin, GPIO.HIGH)
        self.pumpIsRunning = True
        return

    def stop(self) -> None:
        GPIO.output(self.pumpPin, GPIO.LOW)
        self.pumpIsRunning = False
        return