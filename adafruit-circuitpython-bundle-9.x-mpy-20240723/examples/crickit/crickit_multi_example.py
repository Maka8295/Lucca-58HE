# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# This is a mock example showing typical usage of the library for each kind of device.

# Add this import if using stepper motors.
# It will expose constants saying how to step: stepper.FORWARD, stepper.BACKWARD, etc.
from adafruit_motor import stepper

from adafruit_crickit import crickit

# Set servo 1 to 90 degrees
crickit.servo_1.angle = 90

# Change servo settings.
crickit.servo_1.actuation_range = 135
crickit.servo_1.set_pulse_width_range(min_pulse=850, max_pulse=2100)

# You can assign a device to a variable to get a shorter name.
servo_2 = crickit.servo_2
servo_2.throttle = 0

# Run a continous servo on Servo 2 backwards at half speed.
crickit.continuous_servo_2.throttle = -0.5

# Run the motor on Motor 1 terminals at half speed.
crickit.dc_motor_1.throttle = 0.5

# Set Drive 1 terminal to 3/4 strength.
crickit.drive_1.fraction = 0.75

if crickit.touch_1.value:
    print("Touched terminal Touch 1")

# A single stepper motor uses up all the motor terminals.
crickit.stepper_motor.onestep(direction=stepper.FORWARD)

# You can also use the Drive terminals for a stepper motor
crickit.drive_stepper_motor.onestep(direction=stepper.BACKWARD)

# Note: On CPX Crickit, NeoPixel pin is normally connected to A1, not to seesaw,
# so this part of the demo cannot control the NeoPixel terminal.
# Strip or ring of 8 NeoPixels
crickit.init_neopixel(8)
crickit.neopixel.fill((100, 100, 100))
