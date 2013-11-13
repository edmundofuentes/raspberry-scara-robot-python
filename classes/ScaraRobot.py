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
        
        self.a = a # Arm A length
        self.b = b # Arm B length
        
        # Robot coordinates
        self.q1 = 0
        self.q2 = 0
        
        self.updateCoords()

        
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
    
    
    def fromRect(self, x, y):
        '''Converts a Rectangular coordinate to Robot coordinate
        
        @param x float position in x-axis
        @param y float position in y-axis
        
        '''
        pass
    
    
    def moveTo(self, q1, q2):
        pass
    
    
    def updateCoords(self):
        '''Updates the polar and rectangular coordinates according to the robot coordinates
        
        '''
        # Rectangular coordinates
        self.x =
        sefl.y =
        
        # Polar coordinates
        self.c =
        self.r =