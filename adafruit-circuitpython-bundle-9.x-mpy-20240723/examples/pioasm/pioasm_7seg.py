# SPDX-FileCopyrightText: 2022 Jeff Epler, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Drive a 7-segment display entirely from the PIO peripheral

By updating the buffer being written to the display, the shown digits can be changed.

The main program just counts up, looping back to 0000 after 9999.

This example is designed for a Raspberry Pi Pico and bare LED display. For
simplicity, it is wired without any current limiting resistors, instead relying
on a combination of the RP2040's pin drive strength and the 1/4 duty cycle to
limit LED current to an acceptable level, and longevity of the display was not
a priority.

Before integrating a variant of this example code in a project, evaluate
whether your design needs to add current-limiting resistors.

https://www.adafruit.com/product/4864
https://www.adafruit.com/product/865

Wiring:
 * Pico GP15 to LED matrix 1 (E SEG)
 * Pico GP14 to LED matrix 2 (D SEG)
 * Pico GP13 to LED matrix 3 (DP SEG)
 * Pico GP12 to LED matrix 4 (C SEG)
 * Pico GP11 to LED matrix 5 (G SEG)
 * Pico GP10 to LED matrix 6 (COM4)
 * Pico GP9 to LED matrix 7 (COLON COM)
 * Pico GP22 to LED matrix 8 (COLON SEG)
 * Pico GP21 to LED matrix 9 (B SEG)
 * Pico GP20 to LED matrix 10 (COM3)
 * Pico GP19 to LED matrix 11 (COM2)
 * Pico GP18 to LED matrix 12 (F SEG)
 * Pico GP17 to LED matrix 13 (A SEG)
 * Pico GP16 to LED matrix 14 (COM1)
"""

import array
import time
import board
import rp2pio
import adafruit_pioasm

_program = adafruit_pioasm.Program(
    """
    out pins, 14       ; set the pins to their new state
    """
)

# Display Pins 1-7 are GP 15-9
# Display Pins 8-12 are GP 22-16
COM1_WT = 1 << 7
COM2_WT = 1 << 10
COM3_WT = 1 << 11
COM4_WT = 1 << 1
COMC_WT = 1 << 0

SEGA_WT = 1 << 8
SEGB_WT = 1 << 12
SEGC_WT = 1 << 3
SEGD_WT = 1 << 5
SEGE_WT = 1 << 6
SEGF_WT = 1 << 9
SEGG_WT = 1 << 2

SEGDP_WT = 1 << 4
SEGCOL_WT = 1 << 13

ALL_COM = COM1_WT | COM2_WT | COM3_WT | COM4_WT | COMC_WT

SEG_WT = [
    SEGA_WT,
    SEGB_WT,
    SEGC_WT,
    SEGD_WT,
    SEGE_WT,
    SEGF_WT,
    SEGG_WT,
    SEGDP_WT,
    SEGCOL_WT,
]
COM_WT = [COM1_WT, COM2_WT, COM3_WT, COM4_WT, COMC_WT]

DIGITS = [
    0b0111111,  # 0
    0b0000110,  # 1
    0b1011011,  # 2
    0b1001111,  # 3
    0b1100110,  # 4
    0b1101101,  # 5
    0b1111100,  # 6
    0b0000111,  # 7
    0b1111111,  # 8
    0b1101111,  # 9
]


def make_digit_wt(v):
    val = ALL_COM
    seg = DIGITS[v]
    for i in range(8):
        if seg & (1 << i):
            val |= SEG_WT[i]
    return val


DIGITS_WT = [make_digit_wt(i) for i in range(10)]


class SMSevenSegment:
    def __init__(self, first_pin=board.GP9):
        self._buf = array.array("H", (DIGITS_WT[0] & ~COM_WT[i] for i in range(4)))
        self._sm = rp2pio.StateMachine(
            _program.assembled,
            frequency=2000,
            first_out_pin=first_pin,
            out_pin_count=14,
            auto_pull=True,
            pull_threshold=14,
            **_program.pio_kwargs,
        )
        self._sm.background_write(loop=self._buf)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.deinit()

    def deinit(self):
        self._sm.deinit()

    def __setitem__(self, i, v):
        if v is None:
            self._buf[i] = 0
        else:
            self._buf[i] = DIGITS_WT[v] & ~COM_WT[i]

    def set_number(self, number):
        for j in range(4):
            self[3 - j] = number % 10
            number //= 10


def count(start=0):
    val = start
    while True:
        yield val
        val += 1


def main():
    with SMSevenSegment(board.GP9) as s:
        for i in count():
            s.set_number(i)
            time.sleep(0.05)


if __name__ == "__main__":
    main()
