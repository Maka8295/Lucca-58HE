# SPDX-FileCopyrightText: 2021 John Furcean
# SPDX-License-Identifier: MIT

"""I2C ANO rotary encoder with 7 segment display example."""

import board
from adafruit_ht16k33 import segments
from adafruit_seesaw import seesaw, rotaryio, digitalio

# For use with the STEMMA connector on QT Py RP2040
# import busio
# i2c = busio.I2C(board.SCL1, board.SDA1)
# seesaw = seesaw.Seesaw(i2c, 0x49)

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
seesaw = seesaw.Seesaw(i2c, addr=0x49)
display = segments.Seg14x4(i2c, address=0x70)

seesaw_product = (seesaw.get_version() >> 16) & 0xFFFF
print(f"Found product {seesaw_product}")
if seesaw_product != 5740:
    print("Wrong firmware loaded?  Expected 5740")

seesaw.pin_mode(1, seesaw.INPUT_PULLUP)
seesaw.pin_mode(2, seesaw.INPUT_PULLUP)
seesaw.pin_mode(3, seesaw.INPUT_PULLUP)
seesaw.pin_mode(4, seesaw.INPUT_PULLUP)
seesaw.pin_mode(5, seesaw.INPUT_PULLUP)

select = digitalio.DigitalIO(seesaw, 1)
select_held = False
up = digitalio.DigitalIO(seesaw, 2)
up_held = False
left = digitalio.DigitalIO(seesaw, 3)
left_held = False
down = digitalio.DigitalIO(seesaw, 4)
down_held = False
right = digitalio.DigitalIO(seesaw, 5)
right_held = False

encoder = rotaryio.IncrementalEncoder(seesaw)
last_position = None

buttons = [select, up, left, down, right]
button_names = ["Select", "Up", "Left", "Down", "Right"]
button_states = [select_held, up_held, left_held, down_held, right_held]
seven_segment_names = ["SELE", " UP ", "LEFT", "DOWN", "RIGH"]

while True:
    position = encoder.position

    if position != last_position:
        last_position = position
        display.print(f"   {position}")
        print(f"Position: {position}")

    for b in range(5):
        if not buttons[b].value and button_states[b] is False:
            button_states[b] = True
            display.print(seven_segment_names[b])
            print(f"{button_names[b]} button pressed")

        if buttons[b].value and button_states[b] is True:
            button_states[b] = False
            display.print("    ")
            print(f"{button_names[b]} button released")
