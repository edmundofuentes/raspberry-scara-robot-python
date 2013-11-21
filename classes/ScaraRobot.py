#!/usr/bin/env python
# -*- coding: utf-8 -*- 
'''
RASPBERRY-SCARA-ROBOT-PYTHON
ScaraRobot class

2013, Edmundo Fuentes
www.edmundofuentes.com

v1.0
'''

import math
from time import sleep
import threading

from BufferInterface import BufferInterface

class ScaraRobot:
    def __init__(self):
        '''Initialize robot'''
        
        # Robot configuration
        self.a = 200 # Arm A length (mm)
        self.b = 150 # Arm B length (mm)
        
        self.minq1 = -3*math.pi/4
        self.maxq1 = 3*math.pi/4
        
        self.minq2 = -3*math.pi/4
        self.maxq2 = 3*math.pi/4
        
        # Motor resolution
        self.step = 2*math.pi/200 # 200 steps per rev

        # Maximum speed
        self.maxSpeed = 50.0  # Pulses per second (Hz)
        
        # Initialize coordinates
        self.setZero()

        # Clean busy flag
        self.busy = False

        # Initialize the threading objects
        self.t1 = threading.Thread()
        self.t2 = threading.Thread()

        # Initialize GPIO
        self.io = BufferInterface()
        
        # Virtual pin definitions for BufferInterface
        self.pinEnable = 0
        self.pinStep = {'x': 1, 'y': 3, 'z': 5}
        self.pinDir = {'x': 2, 'y': 4, 'z': 6}
        self.pinAux = 7

        # Enabling interface
        self.io.write(self.pinEnable, 0) # TODO: Fix this.
        
        
    def updateCoords(self):
        '''Updates the polar and rectangular coordinates according to the robot coordinates
        
        '''
        
        # Robot step position
        self.s1 = round( self.q1 / self.step )
        self.s2 = round( self.q2 / self.step )
        
        # Robot angles
        self.q1 = self.s1 * self.step
        self.q2 = self.s2 * self.step
        
        # Rectangular coordinates
        self.x = self.a*math.cos(self.q1) + self.b*math.cos(self.q1+self.q2)
        self.y = self.a*math.cos(self.q1) + self.b*math.cos(self.q1+self.q2)
        
        # Polar coordinates
        self.c = self.q1 + self.q2 # shortcut
        self.r = math.sqrt(self.x**2 + self.y**2)
    
    
    def fromRect(self, x, y):
        '''Converts a Rectangular coordinate to Robot coordinate
        
        @param x float position in x-axis
        @param y float position in y-axis
        
        '''
        q2 = math.acos( (x**2 + y**2 - self.a**2 - self.b**2) / (2*self.a*self.b) )
        q1 = math.asin(self.b*math.sin(q2)/math.sqrt(x**2 + y**2)) + math.atan(2*(y/x))
        
        return [q1, q2]
    
    
    def fromPolar(self, c, r):
        '''Convert a Polar coordinate to Robot coordinate
        
        @param c float angle (in rads)
        @param r float radius
        
        '''
        
        # First convert to rectangular coordinates
        # TODO: There should be a more elegant way..
        x = r * math.cos(c)
        y = r * math.sin(c)
        
        return self.fromRect(x, y)
    
    
    def roundCoords(self, qd1, qd2):
        '''Round the given robot coordinates to ones that are valid to the configuration
        
        @param qd1 float desired q1
        @param qd2 float desired q2
        
        '''
        
        q1 = round( qd1 / self.step ) * self.step
        q2 = round( qd2 / self.step ) * self.step
        
        return [q1, q2]
    
    
    def getPosition(self):
        '''Return the current position in a dictionary with the coordinate systems'''
        return {'step': [self.s1, self.s2],
                'robot': [self.q1, self.q2],
                'rect': [self.x, self.y],
                'polar': [self.c, self.r]}

    
    def getPixelPosition(self):
        '''Return the current position in pixels (1mm=1px), centered about (360,360)'''
        x1 = 360 + math.cos(self.q1)*self.a
        y1 = 360 - math.sin(self.q1)*self.a 
        x2 = x1 + math.cos(self.q1 + self.q2)*self.b
        y2 = y1 - math.sin(self.q1 + self.q2)*self.b
        return {'p1': [x1, y1],
                'p2': [x2, y2]}


    def getMaxRange(self):
        '''Return a dictionary with the robot maximum ranges'''
        
        maxR = self.a + self.b
        minR = self.a - self.b
        return {'maxR': maxR,
                'minR': minR,
                'minq1': self.minq1,
                'maxq1': self.maxq1,
                'minq2': self.minq2,
                'maxq2': self.maxq2}
    
    
    def setZero(self):
        ''' Set the current position as zero
        
        Uses by default the configuration q1:0°, q2:0°
        
        '''
        
        # Default zero position
        self.q1 = 0
        self.q2 = 0
        
        self.updateCoords()


    def isBusy(self):
        '''Returns the robot's current busy status'''
        if self.t1.isAlive() or self.t2.isAlive():
            return True
        else:
            return False

    
    def moveTo(self, qd1, qd2):
        
        self.updateCoords()
        
        # Calculate the number of steps
        sd1 = round( qd1 / self.step )
        sd2 = round( qd2 / self.step )

        sm1 = sd1 - self.s1
        sm2 = sd2 - self.s2

        # Get direction of movement
        if sm1 >= 0:
            dir1 = 1
        else:
            dir1 = 0

        if sm2 >= 0:
            dir2 = 1
        else:
            dir2 = 0

        # Make all steps positive
        sm1 = abs(sm1)
        sm2 = abs(sm2)

        # Calculate speeds
        if sm1 == 0:
            # no movement in sm1, max speed in 2
            speed1 = 0
            speed2 = self.maxSpeed
        elif sm2 == 0:
            # no movement in sm2, max speed in 1
            speed1 = self.maxSpeed
            speed2 = 0
        elif sm1 > sm2:
            # more steps on 1, therefore higher speed on 1
            speed1 = self.maxSpeed
            speed2 = float(sm2)/sm1 * self.maxSpeed
        else:
            # more steps on 2, therefore higher speed on 2
            speed1 = float(sm1)/sm2 * self.maxSpeed
            speed2 = self.maxSpeed

        # Run the threads to generate the steps
        if sm1 > 0:
            sm1 = int(sm1)
            self.t1 = threading.Thread(target=self.moveMotor1, args=(sm1, dir1, speed1))
            self.t1.daemon = True
            self.t1.start()

        if sm2 > 0:
            sm2 = int(sm2)
            self.t2 = threading.Thread(target=self.moveMotor2, args=(sm2, dir2, speed2))
            self.t2.daemon = True
            self.t2.start()


    def moveMotor1(self, steps, direction, speed):

        # Write the direction
        self.io.write(self.pinDir['x'], direction)

        delay =  1.0/speed
        
        for i in range(steps):
            self.io.write(self.pinStep['x'], 1)

            if direction: self.q1 = self.q1 + self.step
            else: self.q1 = self.q1 - self.step
            
            sleep(delay/2.0)
            self.io.write(self.pinStep['x'], 0)
            sleep(delay/2.0)
            

    def moveMotor2(self, steps, direction, speed):

        # Write the direction
        self.io.write(self.pinDir['y'], direction)

        delay =  1.0/speed
        
        for i in range(steps):
            self.io.write(self.pinStep['y'], 1)

            if direction: self.q2 = self.q2 + self.step
            else: self.q2 = self.q2 - self.step
            
            sleep(delay/2.0)
            self.io.write(self.pinStep['y'], 0)
            sleep(delay/2.0)
    
    
    
