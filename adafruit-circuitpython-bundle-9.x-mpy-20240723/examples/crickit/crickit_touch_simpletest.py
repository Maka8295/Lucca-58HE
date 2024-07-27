# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Crickit library demo - Capacitive touch

import time

from adafruit_crickit import crickit

while True:
    if crickit.touch_1.value:
        print("Touched terminal Touch 1")
    time.sleep(0.25)
