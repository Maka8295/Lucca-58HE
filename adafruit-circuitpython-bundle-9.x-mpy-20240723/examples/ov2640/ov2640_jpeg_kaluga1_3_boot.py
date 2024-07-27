# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""Use this file as CIRCUITPY/boot.py in conjunction with ov2640_jpeg_kaluga1_3.py

It makes the CIRCUITPY filesystem writable to CircuitPython
(and read-only to the PC) unless the "MODE" button on the audio
daughterboard is held while the board is powered on or reset.
"""

import analogio
import board
import storage

V_MODE = 1.98
V_RECORD = 2.41

a = analogio.AnalogIn(board.IO6)
a_voltage = a.value * a.reference_voltage / 65535  # pylint: disable=no-member
if abs(a_voltage - V_MODE) > 0.05:  # If mode is NOT pressed...
    print("storage writable by CircuitPython")
    storage.remount("/", readonly=False)
