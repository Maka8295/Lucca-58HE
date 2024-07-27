# SPDX-FileCopyrightText: 2022 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
"""Arcade QT example for multiple boards that turns on button LED when button is pressed"""
import board
import digitalio
from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw.digitalio import DigitalIO

# For most boards.
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

# For the QT Py RP2040, QT Py ESP32-S2, other boards that have SCL1/SDA1 as the STEMMA QT port.
# import busio
# i2c = busio.I2C(board.SCL1, board.SDA1)
arcade_qt_one = Seesaw(i2c, addr=0x3A)
arcade_qt_two = Seesaw(i2c, addr=0x3B)

arcade_qts = (arcade_qt_one, arcade_qt_two)

# Button pins in order (1, 2, 3, 4)
button_pins = (18, 19, 20, 2)
buttons = []
for arcade_qt in arcade_qts:
    for button_pin in button_pins:
        button = DigitalIO(arcade_qt, button_pin)
        button.direction = digitalio.Direction.INPUT
        button.pull = digitalio.Pull.UP
        buttons.append(button)

# LED pins in order (1, 2, 3, 4)
led_pins = (12, 13, 0, 1)
leds = []
for arcade_qt in arcade_qts:
    for led_pin in led_pins:
        led = DigitalIO(arcade_qt, led_pin)
        led.direction = digitalio.Direction.OUTPUT
        leds.append(led)

while True:
    for led_number, button in enumerate(buttons):
        leds[led_number].value = not button.value
