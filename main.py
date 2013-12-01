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
import curses
import os

from classes.SnesGamepad import SnesGamepad
from classes.ScaraRobot import ScaraRobot
from classes.BufferInterface import BufferInterface

simulation = False

def main():
    print "## STARTING UP ##"
    
    # Initialize planar SCARA robot instance
    scara = ScaraRobot()
    
    # Initialize GamePad
    j = SnesGamepad()

    # Initialize graphical interface
    if simulation:
        pygame.init()
        window = pygame.display.set_mode((720, 720))
        font = pygame.font.SysFont("freeserif", 20)

    # Initialize operating variables
    coord_mode = 0
    speed = .5
    button_state = j.getButtons()

    # Config advance per button press
    angleStep = math.pi/100.0 # angle
    rectStep = 10.0 # mm
    polarAngleStep = math.pi/40.0
    polarRadiusStep = 10.0 # mm
    
    print "## BEGINNING MAIN LOOP ##"
    k = 0
    error_msg = 0
    while True:
        #### CONTROL OPERATIONS ####
        # Check buttons on gamepad
        old_SELECT = button_state['SELECT']
        old_START = button_state['START']
        old_LEFT = button_state['LEFT']
        old_RIGHT = button_state['RIGHT']
        old_UP = button_state['UP']
        old_DOWN = button_state['DOWN']
        old_A = button_state['A']
        old_B = button_state['B']
        old_X = button_state['X']
        old_Y = button_state['Y']
        old_R = button_state['R']
        old_L = button_state['L']

        button_state = j.getButtons()
        
        # Check coord_mode
        if button_state['START'] == True and old_START == False:
            coord_mode = coord_mode + 1
            if coord_mode == 3: coord_mode = 0
            print "New mode:", repr(coord_mode)

        # Set Zero
        if button_state['SELECT'] == True and old_SELECT == False:
            scara.setZero()
            print "Set zero"

        # Enable Reset
        if button_state['X'] == True: # and old_X == False:
            scara.resetEnable()

        # Check Speeds
        if button_state['L'] == True and old_L == False:
            speed = speed - 0.1
            if speed < 0.1: speed = 0.1

        if button_state['R'] == True and old_R == False:
            speed = speed + 0.1
            if speed >= 1.0: speed = 1.0

        # Toggle Aux
        if button_state['Y'] == True and old_Y == False:
            scara.toggleAux()

        # Vertical Movement
        if not scara.isBusy():
            if button_state['B'] == True:
                scara.moveElevator(1.0)
            elif button_state['A'] == True and old_A == False:
                scara.moveElevatorStep()
        
        # Check if robot is busy (moving)
        if not scara.isBusy():
            if coord_mode == 0:
                # ROBOT COORDINATE MODE
                text_coord_mode = "Robot"
                if button_state['LEFT'] == True:
                    pos = scara.getPosition()['robot']
                    newPos = [pos[0] + angleStep, pos[1]]
                    if scara.getRange()['minq1'] <= newPos[0] <= scara.getRange()['maxq1']:
                        scara.moveTo(newPos[0], newPos[1], speed)
                elif button_state['RIGHT'] == True:
                    pos = scara.getPosition()['robot']
                    newPos = [pos[0] - angleStep, pos[1]]
                    if scara.getRange()['minq1'] <= newPos[0] <= scara.getRange()['maxq1']:
                        scara.moveTo(newPos[0], newPos[1], speed)
                elif button_state['UP'] == True:
                    pos = scara.getPosition()['robot']
                    newPos = [pos[0], pos[1] + angleStep]
                    if scara.getRange()['minq2'] <= newPos[1] <= scara.getRange()['maxq2']:
                        scara.moveTo(newPos[0], newPos[1], speed)
                elif button_state['DOWN'] == True:
                    pos = scara.getPosition()['robot']
                    newPos = [pos[0], pos[1] - angleStep]
                    if scara.getRange()['minq2'] <= newPos[1] <= scara.getRange()['maxq2']:
                        scara.moveTo(newPos[0], newPos[1], speed)

            elif coord_mode == 1:
                # RECTANGULAR COORDINATE MODE
                text_coord_mode = "Rectangular"
                if button_state['LEFT'] == True:
                    pos = scara.getPosition()['rect']
                    pos = [pos[0] - rectStep, pos[1]]
                    if scara.getRange()['minR'] <= math.sqrt(pos[0]**2 + pos[1]**2) <= scara.getRange()['maxR']:
                        qpos = scara.fromRect(pos[0], pos[1])
                        scara.moveTo(qpos[0], qpos[1], speed)
                    else:
                        error_msg = "Out of bounds. Cannot move"
                        
                elif button_state['RIGHT'] == True:
                    pos = scara.getPosition()['rect']
                    pos = [pos[0] + rectStep, pos[1]]
                    if scara.getRange()['minR'] <= math.sqrt(pos[0]**2 + pos[1]**2) <= scara.getRange()['maxR']:
                        qpos = scara.fromRect(pos[0], pos[1])
                        scara.moveTo(qpos[0], qpos[1], speed)
                    else:
                        error_msg = "Out of bounds. Cannot move"
                        
                elif button_state['UP'] == True:
                    pos = scara.getPosition()['rect']
                    pos = [pos[0], pos[1] + rectStep]
                    if scara.getRange()['minR'] <= math.sqrt(pos[0]**2 + pos[1]**2) <= scara.getRange()['maxR']:
                        qpos = scara.fromRect(pos[0], pos[1])
                        scara.moveTo(qpos[0], qpos[1], speed)
                    else:
                        error_msg = "Out of bounds. Cannot move"
                        
                elif button_state['DOWN'] == True:
                    # Move on the negative Y-axis
                    pos = scara.getPosition()['rect']
                    pos = [pos[0], pos[1] - rectStep]
                    if scara.getRange()['minR'] <= math.sqrt(pos[0]**2 + pos[1]**2) <= scara.getRange()['maxR']:
                        qpos = scara.fromRect(pos[0], pos[1])
                        scara.moveTo(qpos[0], qpos[1], speed)
                    else:
                        error_msg = "Out of bounds. Cannot move"

            elif coord_mode == 2:
                # POLAR COORDINATE MODE
                text_coord_mode = "Polar"
                if button_state['LEFT'] == True:
                    pos = scara.getPosition()['polar']
                    pos = [pos[0] + polarAngleStep, pos[1]]
                    if True:
                        qpos = scara.fromPolar(pos[0], pos[1])
                        scara.moveTo(qpos[0], qpos[1], speed)
                    else:
                        error_msg = "Out of bounds. Cannot move"
                        
                elif button_state['RIGHT'] == True:
                    pos = scara.getPosition()['polar']
                    pos = [pos[0] - polarAngleStep, pos[1]]
                    if True:
                        qpos = scara.fromPolar(pos[0], pos[1])
                        scara.moveTo(qpos[0], qpos[1], speed)
                    else:
                        error_msg = "Out of bounds. Cannot move"
                        
                elif button_state['UP'] == True:
                    pos = scara.getPosition()['polar']
                    pos = [pos[0], pos[1] + polarRadiusStep]
                    if scara.getRange()['minR'] <= pos[1] <= scara.getRange()['maxR']:
                        qpos = scara.fromPolar(pos[0], pos[1])
                        scara.moveTo(qpos[0], qpos[1], speed)
                    else:
                        error_msg = "Out of bounds. Cannot move"
                        
                elif button_state['DOWN'] == True:
                    pos = scara.getPosition()['polar']
                    pos = [pos[0], pos[1] - polarRadiusStep]
                    if scara.getRange()['minR'] <= pos[1] <= scara.getRange()['maxR']:
                        qpos = scara.fromPolar(pos[0], pos[1])
                        scara.moveTo(qpos[0], qpos[1], speed)
                    else:
                        error_msg = "Out of bounds. Cannot move"
                
        
        # Move robot. (Check if it's busy)

        #### GRAPHICAL INTERFACE ####
        if simulation:
            # Calculate the pixel coordinates
            scara.updateCoords()
            pxPos = scara.getPixelPosition()

            # Draw the SCARA
            #pygame.draw.rect(window, (0,0,0), pygame.Rect((0,0), (720, 720))) # Clear the screen, look for another way
            pygame.draw.line(window, (255,255,255), (360,360), (pxPos['p1'][0], pxPos['p1'][1]), 4)
            pygame.draw.line(window, (255,122,255), (pxPos['p1'][0], pxPos['p1'][1]), (pxPos['p2'][0], pxPos['p2'][1]), 4)

            # Print the current coordinates on screen
            '''
            pos = scara.getPosition()
            posText = ""
            #posText = posText + "Robot: " + repr(pos['robot'][0]) + "," + repr(pos['robot'][1])
            posText = posText + "; Rect" + repr(pos['rect'][0]) + "," + repr(pos['rect'][1])
            #posText = posText + "; Polar" + repr(pos['polar'][0]) + "," + repr(pos['polar'][1])
            #posText = posText + "; Step" + repr(pos['step'][0]) + "," + repr(pos['step'][1]) 
            textSurface = font.render(posText, 1, pygame.Color(255, 255, 255))
            window.blit(textSurface, (10,10))
            '''

            pygame.display.update( pygame.Rect((0,0), (720, 720)) )

            # Draw over the old lines
            pygame.draw.line(window, (0,0,0), (360,360), (pxPos['p1'][0], pxPos['p1'][1]), 4)
            pygame.draw.line(window, (0,0,0), (pxPos['p1'][0], pxPos['p1'][1]), (pxPos['p2'][0], pxPos['p2'][1]), 4)
            pygame.draw.rect(window, (0,0,0), pygame.Rect((0,0), (720, 30)))
        

        #k = k + 1

        #### TEXT INTERFACE ####
        # Update only once every N cycles
        '''
        if k >= 200:
            os.system('clear')
            k = 0
            pos = scara.getPosition()
            
            print "###  SCARA ROBOT CONTROL INTERFACE  ###"
            print ""
            print "# Coordinates #"
            print "Step: " + repr(pos['step'][0]) + "," + repr(pos['step'][1])
            print "Robot: " + repr(pos['robot'][0]) + "," + repr(pos['robot'][1])
            print "Rect: " + repr(pos['rect'][0]) + "," + repr(pos['rect'][1])
            print "Polar: " + repr(pos['polar'][0]) + "," + repr(pos['polar'][1])
            print ""
            print "# Control #"
            print "Control Mode:", text_coord_mode
            print "Speed:", repr(speed*10), "%"
            print ""
            print "# Status #"
            print "Busy", scara.isBusy()
            print error_msg
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
