raspberry-scara-robot-python
============================

Python libraries, code and tests for a custom built SCARA robot project.  Written for the Raspberry Pi and a TB6560 stepper motor controller.

# Controls
The SCARA robot is controlled by a USB SNES controller.

## Buttons
- Start: Set the current position as zero
- Select: Change between the 3 types of operation modes
- Up/Down: Control Axis 1 (depends on the operation mode)
- Left/Right: Control Axis 2 (depends on the operation mode)
- A: Raise the electromagnet
- B: Lower the electromagnet
- X: Enable the electromagnet
- Y: Disable the electromagnet

# Operation Modes
## Rectangular
- Axis 1: Y axis
- Axis 2: X axis

## Polar
- Axis 1: angle
- Axis 2: radius

## Robot
- Axis 1: motor 1 position
- Axis 2: motor 2 position