raspberry-scara-robot-python
============================

Python libraries, code and tests for a custom built SCARA robot project.  Written for the Raspberry Pi and a TB6560 stepper motor controller.

# Controls
The SCARA robot is controlled by a USB SNES controller.

- *Start*: Change between the 3 types of operation modes
- *Select*: Set the current position as zero
- *Up/Down*: Control Axis 1 (depends on the operation mode)
- *Left/Right*: Control Axis 2 (depends on the operation mode)
<<<<<<< HEAD
- *A*: Change direction of the linear actuator
- *B*: Activate the linear actuator
- *X*: Global motor disable (Safe stop)
- *Y*: Toggle auxiliary relay (electromagnet)
=======
- *L*: Decrease speed
- *R*: Increase speed
- *A*: Raise the electromagnet
- *B*: Lower the electromagnet
- *X*: Enable the electromagnet
- *Y*: Disable the electromagnet
>>>>>>> ea9b5b8f4e557585f73e8f5810518a0f4285fc43

# Operation Modes
## Robot
- *Axis 1*: motor 1 position
- *Axis 2*: motor 2 position

## Rectangular
- *Axis 1*: Y axis
- *Axis 2*: X axis

## Polar
- *Axis 1*: angle
- *Axis 2*: radius
