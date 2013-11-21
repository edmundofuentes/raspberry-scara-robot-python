import pygame
import time

class SnesGamepad:
    def __init__(self):
        print "Initiazing joystick support.."
        pygame.init()

        while pygame.joystick.get_count() == 0:
            print "Waiting for joystick.. count:", pygame.joystick.get_count()
            time.sleep(5)
            pygame.joystick.quit()
            pygame.joystick.init()
    
        try:    
            self.js = pygame.joystick.Joystick(0)
            self.js.init()
            print "Enabled joystick:", self.js.get_name()
        except pygame.error:
            print "Couldn't initialize joystick."
            exit()

        if self.js.get_numbuttons() != 8 or self.js.get_numaxes() != 2:
            print "Wrong joystick recognized! Exiting.."
            exit()

        # Initialize button dictionaries
        self.buttonNames = {0: 'R', 1: 'L', 2: 'X', 3: 'A', 
                            4: 'START', 5: 'SELECT', 6: 'Y', 7: 'B'}
        self.buttonAxisNames = {0: 'HOR', 1: 'VERT'}
        self.buttonStates = {'A': False, 'B': False,
                             'X': False, 'Y': False,
                             'R': False, 'L': False,
                             'START': False, 'SELECT': False,
                             'UP': False, 'DOWN': False,
                             'RIGHT': False, 'LEFT': False}

    def updateState(self):
        # Load the events since last check
        events = pygame.event.get()

        # Parse the events
        for event in events:
            # print event # Debug..
            
            # Check Buttons
            if event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYBUTTONUP:
                button = self.buttonNames[event.button]
                if self.buttonStates[button] == False and event.type == pygame.JOYBUTTONDOWN:
                    self.buttonStates[button] = True
                elif self.buttonStates[button] == True and event.type == pygame.JOYBUTTONUP:
                    self.buttonStates[button] = False
            
            # Check Axis
            if event.type == pygame.JOYAXISMOTION:
                # HORIZONTAL
                if event.axis == 0:
                    if event.value == 0:
                        self.buttonStates['RIGHT'] = False
                        self.buttonStates['LEFT'] = False
                    elif event.value > 0:
                        self.buttonStates['RIGHT'] = True
                        self.buttonStates['LEFT'] = False
                    else:
                        self.buttonStates['RIGHT'] = False
                        self.buttonStates['LEFT'] = True
                # VERTICAL
                elif event.axis == 1:
                    if event.value == 0:
                        self.buttonStates['UP'] = False
                        self.buttonStates['DOWN'] = False
                    elif event.value > 0:
                        self.buttonStates['UP'] = False
                        self.buttonStates['DOWN'] = True
                    else:
                        self.buttonStates['UP'] = True
                        self.buttonStates['DOWN'] = False


    def getButtons(self):
        self.updateState()
        b = self.buttonStates
        return b
