import RPi.GPIO as GPIO

class register:
    "This class controls registers."

    def __init__(self, serialDataPin, serialClockPin, registerClockPin, supportedPots):
        self.serialDataPin = serialDataPin
        self.serialClockPin = serialClockPin
        self.registerClockPin = registerClockPin
        self.supportedPots = supportedPots

        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.serialDataPin, GPIO.OUT)
        GPIO.setup(self.serialClockPin, GPIO.OUT)
        GPIO.setup(self.registerClockPin, GPIO.OUT)


    def pulse(self, outputPin):
        GPIO.output(outputPin, GPIO.LOW)
        GPIO.output(outputPin, GPIO.HIGH)
        GPIO.output(outputPin, GPIO.LOW)


    def clear(self):
        GPIO.output(self.serialDataPin, GPIO.LOW)

        for _ in range(self.supportedPots):
            self.pulse(self.serialClockPin)

        self.pulse(self.registerClockPin)
        print("Register cleared!")


    def setRegisterOutput(self, inputBitstream):
        inputBitstream = inputBitstream[::-1]

        for bit in inputBitstream:
            if(bit == '0'):
                GPIO.output(self.serialDataPin, GPIO.LOW)
            else:
                GPIO.output(self.serialDataPin, GPIO.HIGH)

            self.pulse(self.serialClockPin)
        self.pulse(self.registerClockPin)
        print("Register set to: " + str(inputBitstream))
        