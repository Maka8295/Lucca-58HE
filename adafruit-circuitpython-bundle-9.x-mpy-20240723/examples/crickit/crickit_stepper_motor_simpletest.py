# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Crickit library demo - stepper motor

import time
from adafruit_motor import stepper
from adafruit_crickit import crickit

# Step motor forward and then backward.
while True:
    crickit.stepper_motor.onestep(direction=stepper.FORWARD)
    time.sleep(1)
    crickit.stepper_motor.onestep(direction=stepper.BACKWARD)
    time.sleep(1)
