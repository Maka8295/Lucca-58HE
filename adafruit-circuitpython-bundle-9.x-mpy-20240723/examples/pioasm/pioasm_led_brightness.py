# SPDX-FileCopyrightText: 2021 Jeff Epler, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT
#
# Adapted from the an example in Appendix C of RPi_PiPico_Digital_v10.pdf

import time
import board
import rp2pio
import adafruit_pioasm

led_quarter_brightness = adafruit_pioasm.assemble(
    """
    set pins, 0 [2]
    set pins, 1
"""
)

led_half_brightness = adafruit_pioasm.assemble(
    """
    set pins, 0
    set pins, 1
"""
)

led_full_brightness = adafruit_pioasm.assemble(
    """
    set pins, 1
"""
)

while True:
    sm = rp2pio.StateMachine(
        led_quarter_brightness, frequency=10000, first_set_pin=board.LED
    )
    time.sleep(1)
    sm.deinit()

    sm = rp2pio.StateMachine(
        led_half_brightness, frequency=10000, first_set_pin=board.LED
    )
    time.sleep(1)
    sm.deinit()

    sm = rp2pio.StateMachine(
        led_full_brightness, frequency=10000, first_set_pin=board.LED
    )
    time.sleep(1)
    sm.deinit()
