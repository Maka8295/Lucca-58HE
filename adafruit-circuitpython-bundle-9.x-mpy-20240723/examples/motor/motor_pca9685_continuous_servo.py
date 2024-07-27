# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time

from board import SCL, SDA
import busio

# Import the PCA9685 module. Available in the bundle and here:
#   https://github.com/adafruit/Adafruit_CircuitPython_PCA9685
from adafruit_pca9685 import PCA9685

from adafruit_motor import servo

i2c = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c)
# You can optionally provide a finer tuned reference clock speed to improve the accuracy of the
# timing pulses. This calibration will be specific to each board and its environment. See the
# calibration.py example in the PCA9685 driver.
# pca = PCA9685(i2c, reference_clock_speed=25630710)
pca.frequency = 50

# The pulse range is 750 - 2250 by default.
servo7 = servo.ContinuousServo(pca.channels[7])
# If your servo doesn't stop once the script is finished you may need to tune the
# reference_clock_speed above or the min_pulse and max_pulse timings below.
# servo7 = servo.ContinuousServo(pca.channels[7], min_pulse=750, max_pulse=2250)

print("Forwards")
servo7.throttle = 1
time.sleep(1)

print("Backwards")
servo7.throttle = -1
time.sleep(1)

print("Stop")
servo7.throttle = 0

pca.deinit()
