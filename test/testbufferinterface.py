from BufferInterface import BufferInterface
import time

def main():
    io = BufferInterface()
    
    print "-- Starting main cycle --"
    k = 1.0
    while True:
        print "Frequency:", repr(1.0/k), "Hz"
        for j in range(int(1.0/k)):
            for i in range(8):
                x = 2**i
                io.writeByte(x)
                time.sleep(k)
        
        k = k / 2
        if 1.0 / k > 2**8: k = 1.0

if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print "Ending by KeyboardInterrupt!"
        BufferInterface.cleanup()