# SPDX-FileCopyrightText: 2021 Jeff Epler, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import rp2pio
import adafruit_pioasm

code = adafruit_pioasm.assemble(
    """
.program uart_rx_mini

; Minimum viable 8n1 UART receiver. Wait for the start bit, then sample 8 bits
; with the correct timing.
; IN pin 0 is mapped to the GPIO used as UART RX.
; Autopush must be enabled, with a threshold of 8.

    wait 0 pin 0        ; Wait for start bit
    set x, 7 [10]       ; Preload bit counter, delay until eye of first data bit
bitloop:                ; Loop 8 times
    in pins, 1          ; Sample data
    jmp x-- bitloop [6] ; Each iteration is 8 cycles

"""
)


class RXUART:
    def __init__(self, pin, baudrate=9600):
        self.pio = rp2pio.StateMachine(
            code,
            first_in_pin=pin,
            frequency=8 * baudrate,
            auto_push=True,
            push_threshold=8,
        )

    @property
    def timeout(self):
        return 0

    @property
    def baudrate(self):
        return self.pio.frequency // 8

    @baudrate.setter
    def baudrate(self, frequency):  # pylint: disable=unused-argument
        self.pio.frequency = freqency * 8  # pylint: disable=undefined-variable

    @property
    def in_waiting(self):
        return self.pio.in_waiting

    def read(self, n):
        b = bytearray(n)
        n = self.pio.readinto(b)
        return b[:n]

    def readinto(self, buf):  # pylint: disable=unused-argument
        return self.pio.readinto(n)  # pylint: disable=undefined-variable
