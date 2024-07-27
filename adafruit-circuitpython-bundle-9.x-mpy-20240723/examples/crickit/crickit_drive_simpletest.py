# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Crickit library demo - Drive terminals

import time

from adafruit_crickit import crickit

# For Circuit Playground Express, micro:bit, and RPi Crickit, use:
drive_1 = crickit.drive_1
# For Feather Crickit, use:
# drive_1 = crickit.feather_drive_1

# Turn on Drive 1 for 1 second and then off for 1 second
while True:
    drive_1.fraction = 1.0
    time.sleep(1)
    drive_1.fraction = 0.0
    time.sleep(1)
