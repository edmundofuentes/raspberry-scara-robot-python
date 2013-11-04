from SnesGamepad import SnesGamepad
from BufferInterface import BufferInterface
import time

def main():
    print "-- Start up procedure --"
    io = BufferInterface()
    j = SnesGamepad()
    
    ## MAIN CYCLE ##
    print "-- Starting main cycle --"
    while True:
        buttons = j.getButtons()

        if buttons['A']: io.write(0, 1) 
        else: io.write(0, 0)
        if buttons['B']: io.write(1, 1) 
        else: io.write(1, 0)
        if buttons['X']: io.write(2, 1) 
        else: io.write(2, 0)
        if buttons['Y']: io.write(3, 1) 
        else: io.write(3, 0)
        if buttons['UP']: io.write(4, 1) 
        else: io.write(4, 0)
        if buttons['DOWN']: io.write(5, 1) 
        else: io.write(5, 0)
        if buttons['RIGHT']: io.write(6, 1) 
        else: io.write(6, 0)
        if buttons['LEFT']: io.write(7, 1) 
        else: io.write(7, 0)

        time.sleep(0.05)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Ending by KeyboardInterrupt"
        BufferInterface.cleanup()
    except SystemExit:
        print "Ending by SystemExit!"
        BufferInterface.cleanup()