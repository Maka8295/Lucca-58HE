# SPDX-FileCopyrightText: 2021 Zichao Hou
# SPDX-License-Identifier: MIT

import time
import board
import digitalio
import adafruit_74hc595

# note: D2 port is close to SCK and MOSI pins for Itsy Bitsy M0
latch_pin = digitalio.DigitalInOut(board.D2)
sr = adafruit_74hc595.ShiftRegister74HC595(
    board.SPI(), latch_pin, number_of_shift_registers=2
)

shift_register_pin_num = 10
shift_register_pins = [sr.get_pin(n) for n in range(shift_register_pin_num)]

# turn all pins off
for pin in shift_register_pins:
    pin.value = False

bar_ind_current = 0  # current index
shift_register_pins[bar_ind_current].value = True

while True:
    # iterate through every LED
    bar_ind_last = bar_ind_current
    bar_ind_current = bar_ind_last + 1
    if bar_ind_current <= (shift_register_pin_num - 1):
        shift_register_pins[bar_ind_last].value = False
        shift_register_pins[bar_ind_current].value = True
    else:
        bar_ind_current = 0
        shift_register_pins[bar_ind_last].value = False
        shift_register_pins[bar_ind_current].value = True
    time.sleep(0.1)
