# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Example that iterates through a servo on every channel, sets each to 180 and then back to 0."""
import time
from adafruit_servokit import ServoKit

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=8)

for i in range(len(kit.servo)):  # pylint: disable=consider-using-enumerate
    kit.servo[i].angle = 180
    time.sleep(1)
    kit.servo[i].angle = 0
    time.sleep(1)
