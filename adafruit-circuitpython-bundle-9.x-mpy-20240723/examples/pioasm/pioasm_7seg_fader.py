# SPDX-FileCopyrightText: 2022 Jeff Epler, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Drive a 7-segment display entirely from the PIO peripheral

Each segment is driven with a 'breathing' waveform that runs at its own pace.
It also demonstrates the use of `asyncio` to perform multiple tasks.

This example is designed for a Raspberry Pi Pico and bare LED display. For
simplicity, it is wired without any current limiting resistors, instead relying
on a combination of the RP2040's pin drive strength and the 1/45 duty cycle to
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

import asyncio
import random
import array
import board
import rp2pio
from ulab import numpy as np
import adafruit_pioasm

_pio_source = """
    mov pins, null     ; turn all pins off
    pull
    out pindirs, {n}   ; set the new direction
    pull
    out pins, {n}      ; set the new values
    pull
    out y, 32
delay:
    jmp y--, delay
    """

# Display Pins 1-7 are GP 15-9 [need to re-wire 9]
# Display Pins 8-12 are GP 22-16 [need to re-wire 22]
# GP#       Display#    Function
# 15 (+ 6)   1          E SEG
# 14 (+ 5)   2          D SEG
# 13 (+ 4)   3          DP SEG
# 12 (+ 3)   4          C SEG
# 11 (+ 2)   5          G SEG
# 10 (+ 1)   6          COM4
#  9 (+ 0)   7          COLON COM
# 22 (+13)   8          COLON SEG
# 21 (+12)   9          B SEG
# 20 (+11)  10          COM3
# 19 (+10)  11          COM2
# 18 (+ 9)  12          F SEG
# 17 (+ 8)  13          A SEG
# 16 (+ 7)  14          COM1

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


class LedFader:
    def __init__(
        self, first_pin, pin_count, cathode_weights, anode_weights, levels=64
    ):  # pylint: disable=too-many-arguments
        self._cathode_weights = cathode_weights
        self._anode_weights = anode_weights
        self._stream = array.array("L", [0, 0, 1]) * (
            1 + len(cathode_weights) * len(anode_weights)
        )
        self._levels = levels
        self._max_count = levels * len(self)
        self._total = len(self)

        program = adafruit_pioasm.Program(_pio_source.format(n=pin_count))
        self._sm = rp2pio.StateMachine(  # pylint: disable=too-many-arguments
            program.assembled,
            frequency=125_000_000,
            first_out_pin=first_pin,
            out_pin_count=14,
            auto_pull=True,
            pull_threshold=14,
            **program.pio_kwargs,
        )
        print(
            f"Note: approximate refresh rate {self._sm.frequency / self._max_count:.0f}Hz"
        )
        self._sm.background_write(loop=self._stream)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.deinit()

    def deinit(self):
        self._sm.deinit()

    def __setitem__(self, i, v):
        if not 0 <= v < self._levels:
            raise ValueError()

        c = i % len(self._cathode_weights)
        r = i // len(self._cathode_weights)
        if not v:
            self._total = self._total - self._stream[3 * i + 2] + 1
            self._stream[3 * i] = 0
            self._stream[3 * i + 1] = 0
            self._stream[3 * i + 2] = 1
        else:
            self._total = self._total - self._stream[3 * i + 2] + v
            self._stream[3 * i] = self._cathode_weights[c] | self._anode_weights[r]
            self._stream[3 * i + 1] = self._cathode_weights[c]
            self._stream[3 * i + 2] = v
        self._stream[3 * len(self) + 2] = self._max_count - self._total

    def __len__(self):
        return len(self._stream) // 3 - 1


class CyclicSignal:
    def __init__(self, data, phase=0):
        self._data = data
        self._phase = 0
        self.phase = phase
        self._scale = len(self._data) - 1

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, value):
        self._phase = value % 1

    @property
    def value(self):
        idxf = self._phase * len(self._data)
        idx = int(idxf)
        frac = idxf % 1
        idx1 = (idx + 1) % len(self._data)
        val = self._data[idx]
        val1 = self._data[idx1]
        return val + (val1 - val) * frac

    def advance(self, delta):
        self._phase = (self._phase + delta) % 1


sine = (np.sin(np.linspace(0, 2 * np.pi, 50, endpoint=False)) * 0.5 + 0.5) ** 2.2 * 64


async def segment_throbber(c, i):
    signal = CyclicSignal(sine, random.random())
    velocity = random.random() * 0.04 + 0.005

    while True:
        signal.advance(velocity)
        c[i] = int(signal.value)
        await asyncio.sleep(0)


async def main():
    with LedFader(
        board.GP9,
        14,
        (
            SEGA_WT,
            SEGB_WT,
            SEGC_WT,
            SEGD_WT,
            SEGE_WT,
            SEGF_WT,
            SEGG_WT,
            SEGDP_WT,
            SEGCOL_WT,
        ),
        (COM1_WT, COM2_WT, COM3_WT, COM4_WT, COMC_WT),
    ) as c:
        await asyncio.gather(*(segment_throbber(c, i) for i in range(len(c))))


asyncio.run(main())
