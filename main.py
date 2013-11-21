#!/usr/bin/env python
# -*- coding: utf-8 -*- 
'''
RASPBERRY-SCARA-ROBOT-PYTHON
ScaraRobot class

2013, Edmundo Fuentes
www.edmundofuentes.com

v1.0
'''
import pygame
import math

from pprint import pprint

from classes.SnesGamepad import SnesGamepad
from classes.ScaraRobot import ScaraRobot
from classes.BufferInterface import BufferInterface


def main():
    print "## STARTING UP ##"
    
    # Initialize planar SCARA robot instance
    scara = ScaraRobot()
    
    # Initialize GamePad
    j = SnesGamepad()

    # Initialize graphical interface
    '''
    pygame.init()
    window = pygame.display.set_mode((1000, 720))
    font = pygame.font.SysFont("freeserif", 20)
    '''

    # Initialize operating variables
    coord_mode = 0
    speed = 5
    button_state = j.getButtons()

    # Config advance per button press
    angleStep = math.pi/40.0 # angle
    rectStep = 1.0 # mm
    polarAngleStep = math.pi/20.0
    polarRadiusStep = 2.0 # mm
    
    print "## BEGINNING MAIN LOOP ##"
    while True:
        #### CONTROL OPERATIONS ####
        # Check buttons on gamepad
        old_SELECT = button_state['SELECT']
        old_START = button_state['START']
        old_LEFT = button_state['LEFT']
        old_RIGHT = button_state['RIGHT']
        old_UP = button_state['UP']
        old_DOWN = button_state['DOWN']
        old_R = button_state['R']
        old_L = button_state['L']

        button_state = j.getButtons()

        
        # Check coord_mode
        if button_state['SELECT'] == True and old_SELECT == False:
            coord_mode = coord_mode + 1
            if coord_mode == 3: coord_mode = 0
            print "Changed to coordinates", repr(coord_mode)

        # Set Zero
        if button_state['START'] == True and old_START == False:
            scara.setZero()
            print "Setting current position as zero"

        # Check Speeds
        if button_state['L'] == True and old_L == False:
            speed = speed - 1
            if speed < 0: speed = 0
            print "Decreasing speed", repr(speed)

        if button_state['R'] == True and old_R == False:
            speed = speed + 1
            if speed >= 10: speed = 10
            print "Increasing speed", repr(speed)
        
        # Check if robot is busy (moving)
        if not scara.isBusy():
            if coord_mode == 0:
                # ROBOT COORDINATE MODE
                if button_state['LEFT'] == True:
                    pos = scara.getPosition()['robot']
                    scara.moveTo(pos[0] + angleStep, pos[1])
                elif button_state['RIGHT'] == True:
                    pos = scara.getPosition()['robot']
                    scara.moveTo(pos[0] - angleStep, pos[1])
                elif button_state['UP'] == True:
                    pos = scara.getPosition()['robot']
                    scara.moveTo(pos[0], pos[1] + angleStep)
                elif button_state['DOWN'] == True:
                    pos = scara.getPosition()['robot']
                    scara.moveTo(pos[0], pos[1] - angleStep)

            elif coord_mode == 1:
                # RECTANGULAR COORDINATE MODE
                if button_state['LEFT'] == True and old_LEFT == False:
                    pos = scara.getPosition()['rect']
                    print pos
                    pos = [pos[0] - rectStep, pos[1]]
                    print pos
                    if scara.getMaxRange()['minR'] <= math.sqrt(pos[0]**2 + pos[1]**2) <= scara.getMaxRange()['maxR']:
                        qpos = scara.fromRect(pos[0], pos[1])
                        scara.moveTo(qpos[0], qpos[1])
                    else:
                        print "Out of bounds. Cannot move"
                        
                elif button_state['RIGHT'] == True and old_RIGHT == False:
                    pos = scara.getPosition()['rect']
                    pos = [pos[0] + rectStep, pos[1]]
                    if scara.getMaxRange()['minR'] <= math.sqrt(pos[0]**2 + pos[1]**2) <= scara.getMaxRange()['maxR']:
                        qpos = scara.fromRect(pos[0], pos[1])
                        print pos
                        scara.moveTo(qpos[0], qpos[1])
                    else:
                        print "Out of bounds. Cannot move"
                        
                elif button_state['UP'] == True and old_UP == False:
                    pos = scara.getPosition()['rect']
                    pos = [pos[0], pos[1] + rectStep]
                    if scara.getMaxRange()['minR'] <= math.sqrt(pos[0]**2 + pos[1]**2) <= scara.getMaxRange()['maxR']:
                        qpos = scara.fromRect(pos[0], pos[1])
                        print pos
                        scara.moveTo(qpos[0], qpos[1])
                    else:
                        print "Out of bounds. Cannot move"
                        
                elif button_state['DOWN'] == True and old_DOWN == False:
                    # Move on the negative Y-axis
                    pos = scara.getPosition()['rect']
                    pos = [pos[0], pos[1] - rectStep]
                    if scara.getMaxRange()['minR'] <= math.sqrt(pos[0]**2 + pos[1]**2) <= scara.getMaxRange()['maxR']:
                        qpos = scara.fromRect(pos[0], pos[1])
                        print pos
                        scara.moveTo(qpos[0], qpos[1])
                    else:
                        print "Out of bounds. Cannot move"
                        
        else:
            #print "busy"
            pass
        
        # Move robot. (Check if it's busy)

        #### GRAPHICAL INTERFACE ####
        '''
        # Calculate the pixel coordinates
        scara.updateCoords()
        pxPos = scara.getPixelPosition()

        # Draw the SCARA
        #pygame.draw.rect(window, (0,0,0), pygame.Rect((0,0), (720, 720))) # Clear the screen, look for another way
        pygame.draw.line(window, (255,255,255), (360,360), (pxPos['p1'][0], pxPos['p1'][1]), 4)
        pygame.draw.line(window, (255,122,255), (pxPos['p1'][0], pxPos['p1'][1]), (pxPos['p2'][0], pxPos['p2'][1]), 4)

        # Print the current coordinates on screen
        pos = scara.getPosition()
        posText = "Robot: " + repr(pos['robot'][0]) + "," + repr(pos['robot'][1])
        posText = posText + "; Rect" + repr(pos['rect'][0]) + "," + repr(pos['rect'][1])
        posText = posText + "; Polar" + repr(pos['polar'][0]) + "," + repr(pos['polar'][1])
        posText = posText + "; Step" + repr(pos['step'][0]) + "," + repr(pos['step'][1]) 
        textSurface = font.render(posText, 1, pygame.Color(255, 255, 255))
        window.blit(textSurface, (10,10))

        pygame.display.update( pygame.Rect((0,0), (720, 720)) )

        # Draw over the old lines
        pygame.draw.line(window, (0,0,0), (360,360), (pxPos['p1'][0], pxPos['p1'][1]), 4)
        pygame.draw.line(window, (0,0,0), (pxPos['p1'][0], pxPos['p1'][1]), (pxPos['p2'][0], pxPos['p2'][1]), 4)
        pygame.draw.rect(window, (0,0,0), pygame.Rect((0,0), (720, 30)))
        '''
        
        

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Ending by KeyboardInterrupt"
        BufferInterface.cleanup()
    except SystemExit:
        print "Ending by SystemExit"
        BufferInterface.cleanup()
