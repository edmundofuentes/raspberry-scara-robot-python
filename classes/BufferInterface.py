import RPi.GPIO as GPIO

class BufferInterface:
    def __init__(self):
        # Define GPIO pins being used
        GPIO.setmode(GPIO.BCM) # Using BCM numbers.
        self.pins = {0: 18, 1: 23, 2: 24, 3: 25, 
                     4:  8, 5: 11, 6:  9, 7: 10}
        
        # GPIO Configuration modes
        GPIO.setwarnings(False)
        
        # Initialize GPIO ports
        print "Initializing GPIOs:",
        for bit in self.pins:
            print self.pins[bit],
            GPIO.setup(self.pins[bit], GPIO.OUT)
            GPIO.output(self.pins[bit], 0)           
        print "done."
    
    def write(self, pin, bit):
        if (0 <= pin <= 7) and (bit == 0 or bit == 1):
            GPIO.output(self.pins[pin], bit)
        else:
            # TODO: Throw exception
            pass
    
    writeBit = write # Alias for write
    
    def writeByte(self, byte):
        for i in range(8):
            bit = (byte >> i) & 1
            GPIO.output(self.pins[i], bit)
    
    @staticmethod
    def cleanup():
        # Safer way, this sets back the pins to input
        #   the problem is that the buffer sees them
        #   as HIGH and could have undesirable effects.
        print "GPIO Cleanup..",       
        GPIO.cleanup()
        print "done."
    