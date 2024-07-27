# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This example plays two tones for 1 second each. Note that the tones are not in a loop - this is
to prevent them from playing indefinitely!"""
from adafruit_circuitplayground import cp

cp.play_tone(262, 1)
cp.play_tone(294, 1)
