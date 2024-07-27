# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import digitalio
import adafruit_74hc595

latch_pin = digitalio.DigitalInOut(board.D5)
sr = adafruit_74hc595.ShiftRegister74HC595(board.SPI(), latch_pin)

# Create the pin objects in a list
pins = [sr.get_pin(n) for n in range(8)]

while True:
    for _ in range(2):  # Run the chase animation twice
        for enabled_pin in range(len(pins)):
            for pin_number, pin in enumerate(pins):
                if pin_number == enabled_pin:
                    pin.value = True
                else:
                    pin.value = False
                time.sleep(0.01)
    for _ in range(3):  # Run the blink animation three times
        for pin in pins:
            pin.value = True
        time.sleep(0.5)
        for pin in pins:
            pin.value = False
        time.sleep(0.5)
