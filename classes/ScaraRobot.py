'''
RASPBERRY-SCARA-ROBOT-PYTHON
ScaraRobot class

2013, Edmundo Fuentes
www.edmundofuentes.com

v1.0
'''


class ScaraRobot:
    def __init__(self, a, b):
        self.a = a # Arm A length
        self.b = b # Arm B length
        
        self.q1 = q1 # Motor 1 position
        self.q2 = q2 # Motor 2 position
        
    def getPolar(self, x, y):
        pass
    
    def getRect(self, q1, q2):
        pass