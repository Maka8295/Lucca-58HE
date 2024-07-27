# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Crickit library demo - servos

import time
from adafruit_crickit import crickit

# Move servo back and forth 180 degrees.
while True:
    crickit.servo_1.angle = 0
    time.sleep(1)
    crickit.servo_1.angle = 180
    time.sleep(1)
