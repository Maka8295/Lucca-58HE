# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Crickit library demo - DC motor

import time
from adafruit_crickit import crickit

# Run motor on Motor 1 terminals forward at full speed and then backward at half speed.
while True:
    crickit.dc_motor_1.throttle = 1.0
    time.sleep(1)
    crickit.dc_motor_1.throttle = -0.5
    time.sleep(1)
