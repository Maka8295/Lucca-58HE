# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
'square_demo.py'.

=================================================
toggles the builtin LED using a square wave
"""
import time
import digitalio
import board
from adafruit_waveform import square

LED = digitalio.DigitalInOut(board.D13)
LED.switch_to_output()
SAMPLE_SQUARE = square.square_wave(2)

while True:
    for i in range(len(SAMPLE_SQUARE)):
        LED.value = i
        print(LED.value)
        time.sleep(0.5)
