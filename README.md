raspberry-scara-robot-python
============================

Python libraries, code and tests for a custom built SCARA robot project.  Written for the Raspberry Pi and a TB6560 stepper motor controller.

# Controls
The SCARA robot is controlled by a USB SNES controller.

- **Start**: Change between the 3 types of operation modes
- **Select**: Set the current position as zero
- **Up/Down**: Control Axis 1 (depends on the operation mode)
- **Left/Right**: Control Axis 2 (depends on the operation mode)
- **L**: Decrease speed
- **R**: Increase speed
- **A**: Change direction of the linear actuator
- **B**: Activate the linear actuator
- **X**: Global motor disable (Safe stop)
- **Y**: Toggle auxiliary relay (electromagnet)

# Operation Modes
## Robot
- **Axis 1**: motor 1 position
- **Axis 2**: motor 2 position

## Rectangular
- **Axis 1**: Y axis
- **Axis 2**: X axis

## Polar
- **Axis 1**: angle
- **Axis 2**: radius
