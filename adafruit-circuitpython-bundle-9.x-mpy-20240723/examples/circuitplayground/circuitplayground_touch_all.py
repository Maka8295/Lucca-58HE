# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This example prints to the serial console when you touch the capacitive touch pads."""
import time
import board
from adafruit_circuitplayground import cp


# You'll need to first use the touchpads individually to register them as active touchpads
# You don't have to use the result though
is_a1_touched = cp.touch_A1  # This result can be used if you want
if is_a1_touched:
    print("A1 was touched upon startup!")
is_a2_touched = cp.touch_A2
is_a3_touched = cp.touch_A3
is_a4_touched = cp.touch_A4

print("Pads that are currently setup as touchpads:")
print(cp.touch_pins)

while True:
    current_touched = cp.touched

    if current_touched:
        print("Touchpads currently registering a touch:")
        print(current_touched)
    else:
        print("No touchpads are currently registering a touch.")

    if all(pad in current_touched for pad in (board.A2, board.A3, board.A4)):
        print("This only prints when A2, A3, and A4 are being held at the same time!")

    time.sleep(0.25)
