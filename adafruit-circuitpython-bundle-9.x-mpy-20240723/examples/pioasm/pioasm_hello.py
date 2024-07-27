# SPDX-FileCopyrightText: 2021 Jeff Epler, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT
#
# Adapted from the example https://github.com/raspberrypi/pico-examples/tree/master/pio/hello_pio

import time
import board
import rp2pio
import adafruit_pioasm

hello = """
.program hello
loop:
    pull
    out pins, 1
; This program uses a 'jmp' at the end to follow the example.  However,
; in a many cases (including this one!) there is no jmp needed at the end
; and the default "wrap" behavior will automatically return to the "pull"
; instruction at the beginning.
    jmp loop
"""

assembled = adafruit_pioasm.assemble(hello)

sm = rp2pio.StateMachine(
    assembled,
    frequency=2000,
    first_out_pin=board.LED,
)
print("real frequency", sm.frequency)

while True:
    sm.write(bytes((1,)))
    time.sleep(0.5)
    sm.write(bytes((0,)))
    time.sleep(0.5)
