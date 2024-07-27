# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
'tone_demo.py'.

=================================================
a short piezo song using tone()
"""
import time
import board
import simpleio


while True:
    for f in (262, 294, 330, 349, 392, 440, 494, 523):
        simpleio.tone(board.A0, f, 0.25)
    time.sleep(1)
