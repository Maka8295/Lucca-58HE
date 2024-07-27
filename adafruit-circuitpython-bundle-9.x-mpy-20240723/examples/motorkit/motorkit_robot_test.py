# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple two DC motor robot class usage example.
# Author: Tony DiCola, Chris Anderron
# License: MIT License https://opensource.org/licenses/MIT
import time

# Import the motorkit_robot.py file (must be in the same directory as this file!).
import motorkit_robot


# Set the trim offset for each motor (left and right).  This is a value that
# will offset the speed of movement of each motor in order to make them both
# move at the same desired speed.  Because there's no feedback the robot doesn't
# know how fast each motor is spinning and the robot can pull to a side if one
# motor spins faster than the other motor.  To determine the trim values move the
# robot forward slowly (around 100 speed) and watch if it veers to the left or
# right.  If it veers left then the _right_ motor is spinning faster so try
# setting RIGHT_TRIM to a small negative value, like -0.05, to slow down the right
# motor.  Likewise if it veers right then adjust the _left_ motor trim to a small
# negative value.  Increase or decrease the trim value until the bot moves
# straight forward/backward.
LEFT_TRIM = 0
RIGHT_TRIM = 0


# Create an instance of the robot with the specified trim values.

robot = motorkit_robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)

# Now move the robot around!
# Each call below takes two parameters:
#  - speed: The speed of the movement, a value from -1.0 to +1.0.  The higher the value
#           the faster the movement.  You need to start with a value around 0.10
#           to get enough torque to move the robot.
#  - time (seconds):  Amount of time to perform the movement.  After moving for
#                     this amount of seconds the robot will stop.  This parameter
#                     is optional and if not specified the robot will start moving
#                     forever.

robot.left(0.5, 1)
robot.right(0.5, 1)
robot.steer(0.5, 0.2)
time.sleep(3)
robot.stop()  # Stop the robot from moving.


# That's it!  Note that on exit the robot will automatically stop moving.
