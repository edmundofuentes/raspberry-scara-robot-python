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

class ScaraRobot:
    def __init__(self, a, b):
        '''Initialize robot
        
        @param a float lenght of arm A
        @param b float lenght of arm B
        
        '''
        
        # Robot configuration
        self.a = a # Arm A length
        self.b = b # Arm B length
        
        self.minq1 = -3*math.pi/4
        self.maxq1 = 3*math.pi/4
        
        self.minq2 = -3*math.pi/4
        self.maxq2 = 3*math.pi/4
        
        # Motor resolution
        self.step = 2*math.pi/200 # 200 steps per rev
        
        # Initialize coordinates
        self.setZero()
        
        
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
        sefl.y = self.a*math.cos(self.q1) + self.b*math.cos(self.q1+self.q2)
        
        # Polar coordinates
        self.c = self.q1 + self.q2 # shortcut
        self.r = math.sqrt(self.x**2 + self.y**2)
    
    
    def fromRect(self, x, y):
        '''Converts a Rectangular coordinate to Robot coordinate
        
        @param x float position in x-axis
        @param y float position in y-axis
        
        '''
        q2 = math.acos( (x**2 + y**2 - self.a**2 - self.b**2) / (2*self.a*self.b) )
        q1 = math.asin(self.b*sin(q2)/sqrt(x**2 + y**2)) + atan(2*(y/x))
        
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


    def getMaxRange(self):
        '''Return a dictionary with the robot maximum ranges'''
        
        maxR = self.a + self.b
        return {'maxR': maxR,
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

    
    def moveTo(self, q1, q2):
        pass
    
    
    