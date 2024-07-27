# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
'sine_demo.py'.

=================================================
toggles the builtin LED using a sine wave
"""
import time
import board
import digitalio
from adafruit_waveform import sine

LED = digitalio.DigitalInOut(board.D13)
LED.switch_to_output()

SINE_SAMPLE = sine.sine_wave(150, 50)

while True:
    for i in range(len(SINE_SAMPLE)):
        LED.value = i
        print(LED.value)
        time.sleep(0.50)
