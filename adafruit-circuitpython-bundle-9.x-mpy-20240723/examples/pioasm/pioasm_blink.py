# SPDX-FileCopyrightText: 2021 Jeff Epler, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT
#
# Adapted from the example https://github.com/raspberrypi/pico-examples/tree/master/pio/pio_blink

import array
import time
import board
import rp2pio
import adafruit_pioasm

blink = adafruit_pioasm.assemble(
    """
.program blink
    pull block    ; These two instructions take the blink duration
    out y, 32     ; and store it in y
forever:
    mov x, y
    set pins, 1   ; Turn LED on
lp1:
    jmp x-- lp1   ; Delay for (x + 1) cycles, x is a 32 bit number
    mov x, y
    set pins, 0   ; Turn LED off
lp2:
    jmp x-- lp2   ; Delay for the same number of cycles again
    jmp forever   ; Blink forever!
"""
)


while True:
    for freq in [5, 8, 30]:
        with rp2pio.StateMachine(
            blink,
            frequency=125_000_000,
            first_set_pin=board.LED,
            wait_for_txstall=False,
        ) as sm:
            data = array.array("I", [sm.frequency // freq])
            sm.write(data)
            time.sleep(3)
        time.sleep(0.5)
