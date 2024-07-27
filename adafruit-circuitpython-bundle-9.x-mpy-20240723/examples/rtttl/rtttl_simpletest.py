# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# The MIT License (MIT)
#
# Copyright (c) 2017 Scott Shawcroft for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# This is tested on the CircuitPlayground Express

import digitalio
import board
import adafruit_rtttl

enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
enable.switch_to_output(value=True)

adafruit_rtttl.play(
    board.SPEAKER,
    "itchy:d=8,o=6,b=160:c,a5,4p,c,a,4p,c,a5,c,a5,"
    + "c,a,4p,p,c,d,e,p,e,f,g,4p,d,c,4d,f,4a#,4a,2c7",
)
adafruit_rtttl.play(
    board.SPEAKER,
    "Phantom:d=4,o=5,b=140:c,f,c,d#.,8c#,2c#,a#4,"
    + "d#,8a#4,2c,c,f,c,d#.,8c#,2c#,a#4,d#.,8a#4,2c,p,c,f,g#,c.6,8a#,2a#,a#,d#.6,8a#,"
    + "2c6,p,c6,2f.6,8d#6,8c#6,8c6,8a#,8g#,8g,8f,2e,c#,c#.,8c,2c",
)
