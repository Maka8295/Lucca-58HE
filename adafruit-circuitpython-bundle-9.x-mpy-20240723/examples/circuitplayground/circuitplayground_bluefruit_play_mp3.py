# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example plays mp3 audio files from the built-in speaker when the A or B buttons are pressed.

NOTE: This example does NOT support Circuit Playground Express.
"""
from adafruit_circuitplayground import cp

while True:
    if cp.button_a:
        cp.play_mp3("dip.mp3")
    if cp.button_b:
        cp.play_mp3("rise.mp3")
