# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Crickit library demo - NeoPixel terminal
# Note: On CPX Crickit, NeoPixel pin is normally connected to A1, not to seesaw,
# so this demo would not control the NeoPixel terminal.
# On the Crickit FeatherWing, the NeoPixel terminal is controlled by seesaw.

# pylint can't figure out "np" can be indexed.
# pylint: disable=unsupported-assignment-operation

import time
from adafruit_crickit import crickit

# Strip or ring of 8 NeoPixels
crickit.init_neopixel(8)

crickit.neopixel.fill(0)

# Assign to a variable to get a short name and to save time.
np = crickit.neopixel

while True:
    np.fill(0)
    time.sleep(1)
    np[0] = (100, 0, 0)
    np[1] = (0, 100, 0)
    np[2] = (0, 0, 100)
    time.sleep(1)
    np.fill((100, 100, 100))
    time.sleep(1)
