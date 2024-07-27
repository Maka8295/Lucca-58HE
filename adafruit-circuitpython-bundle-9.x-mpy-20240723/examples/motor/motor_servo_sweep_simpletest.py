# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import pwmio
from adafruit_motor import servo

# create a PWMOut object on the control pin.
pwm = pwmio.PWMOut(board.D5, duty_cycle=0, frequency=50)

# To get the full range of the servo you will likely need to adjust the min_pulse and max_pulse to
# match the stall points of the servo.
# This is an example for the Sub-micro servo: https://www.adafruit.com/product/2201
# servo = servo.Servo(pwm, min_pulse=580, max_pulse=2350)
# This is an example for the Micro Servo - High Powered, High Torque Metal Gear:
#   https://www.adafruit.com/product/2307
# servo = servo.Servo(pwm, min_pulse=500, max_pulse=2600)
# This is an example for the Standard servo - TowerPro SG-5010 - 5010:
#   https://www.adafruit.com/product/155
# servo = servo.Servo(pwm, min_pulse=400, max_pulse=2400)
# This is an example for the Analog Feedback Servo: https://www.adafruit.com/product/1404
# servo = servo.Servo(pwm, min_pulse=600, max_pulse=2500)
# This is an example for the Micro servo - TowerPro SG-92R: https://www.adafruit.com/product/169
# servo = servo.Servo(pwm, min_pulse=500, max_pulse=2400)

# The pulse range is 750 - 2250 by default. This range typically gives 135 degrees of
# range, but the default is to use 180 degrees. You can specify the expected range if you wish:
# servo = servo.Servo(board.D5, actuation_range=135)
servo = servo.Servo(pwm)

# We sleep in the loops to give the servo time to move into position.
print("Sweep from 0 to 180")
for i in range(180):
    servo.angle = i
    time.sleep(0.01)
print("Sweep from 180 to 0")
for i in range(180):
    servo.angle = 180 - i
    time.sleep(0.01)

print("Move to 90 degrees")
servo.angle = 90
time.sleep(1)
print("Release servo motor for 10 seconds")
servo.fraction = None
time.sleep(10)

# You can also specify the movement fractionally.
print("Sweep from 0 to 1.0 fractionally")
fraction = 0.0
while fraction < 1.0:
    servo.fraction = fraction
    fraction += 0.01
    time.sleep(0.01)
