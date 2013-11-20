from classes.SnesGamepad import SnesGamepad
from classes.ScaraRobot import ScaraRobot
from classes.ElevatorRobot import ElevatorRobot
from classes.BufferInterface import BufferInterface

def setup():
    print "## STARTING UP ##"
    
    # Initialize planar SCARA robot instance
    scara = ScaraRobot()
    
    # Initialize elevator instance
    elev = ElevatorRobot()
    
    # Initialize GamePad
    j = SnesGamepad()
    
    # Initialize operating variables
    coord_mode = 0
    
def main():
    print "## BEGGNING MAIN LOOP ##"
    while True:
        # Check buttons on gamepad
        
        # Debounce
        
        # Check coord_mode
        
        # Calculate new position
        
        # Move robot. (Check if it's busy)
        
        
        pass

if __name__ == '__main__':
    try:
        setup()
        main()
    except KeyboardInterrupt:
        print "Ending by KeyboardInterrupt"
        BufferInterface.cleanup()
    except SystemExit:
        print "Ending by SystemExit"
        BufferInterface.cleanup()
