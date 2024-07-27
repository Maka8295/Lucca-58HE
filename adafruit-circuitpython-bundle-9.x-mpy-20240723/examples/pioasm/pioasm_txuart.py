# SPDX-FileCopyrightText: 2021 Jeff Epler, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import rp2pio
import adafruit_pioasm

code = adafruit_pioasm.Program(
    """
.program uart_tx
.side_set 1 opt

; An 8n1 UART transmit program.
; OUT pin 0 and side-set pin 0 are both mapped to UART TX pin.

  pull side 1 [7] ; Assert stop bit, or stall with line in idle state
  set x, 7 side 0 [7] ; Preload bit counter, assert start bit for 8 clocks
bitloop: ; This loop will run 8 times (8n1 UART)
  out pins, 1 ; Shift 1 bit from OSR to the first OUT pin
  jmp x-- bitloop [6] ; Each loop iteration is 8 cycles.

"""
)


class TXUART:
    def __init__(self, *, tx, baudrate=9600):
        self.pio = rp2pio.StateMachine(
            code.assembled,
            first_out_pin=tx,
            first_sideset_pin=tx,
            frequency=8 * baudrate,
            initial_sideset_pin_state=1,
            initial_sideset_pin_direction=1,
            initial_out_pin_state=1,
            initial_out_pin_direction=1,
            **code.pio_kwargs,
        )

    @property
    def timeout(self):
        return 0

    @property
    def baudrate(self):
        return self.pio.frequency // 8

    @baudrate.setter
    def baudrate(self, frequency):
        self.pio.frequency = frequency * 8

    def write(self, buf):
        return self.pio.write(buf)
