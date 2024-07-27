# SPDX-FileCopyrightText: 2021 Scott Shawcroft, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
import rp2pio
import board
import adafruit_pioasm

squarewave = """
.program squarewave
    set pins 1      ; Drive pin high and then delay for one cycle
    set pins 0      ; Drive pin low
"""

assembled = adafruit_pioasm.assemble(squarewave)

sm = rp2pio.StateMachine(
    assembled,
    frequency=1000 * 2,
    first_set_pin=board.D13,
)
print("real frequency", sm.frequency)

time.sleep(120)
