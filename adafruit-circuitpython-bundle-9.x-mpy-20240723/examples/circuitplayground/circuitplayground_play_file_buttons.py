# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""THIS EXAMPLE REQUIRES A WAV FILE FROM THE examples FOLDER IN THE
Adafruit_CircuitPython_CircuitPlayground REPO found at:
https://github.com/adafruit/Adafruit_CircuitPython_CircuitPlayground/tree/main/examples

Copy the "dip.wav" and "rise.wav" files to your CIRCUITPY drive.

Once the files are copied, this example plays a different wav file for each button pressed!"""
from adafruit_circuitplayground import cp

while True:
    if cp.button_a:
        cp.play_file("dip.wav")
    if cp.button_b:
        cp.play_file("rise.wav")
