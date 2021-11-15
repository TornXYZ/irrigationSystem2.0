import RPi.GPIO as GPIO

class pump:
    "This class controls the pump."

    def __init__(self, pump_pin: int) -> None:
        self.pump_pin = pump_pin
        self.pump_is_running = False

        self.setup()
        return

    def setup(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pump_pin, GPIO.OUT)
        return

    def start(self) -> None:
        GPIO.output(self.pump_pin, GPIO.HIGH)
        self.pump_is_running = True
        return

    def stop(self) -> None:
        GPIO.output(self.pump_pin, GPIO.LOW)
        self.pump_is_running = False
        return