# SPDX-FileCopyrightText: 2022 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
"""Arcade QT example that pulses the button LED on button press"""
import time
import board
import digitalio
from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw.digitalio import DigitalIO
from adafruit_seesaw.pwmout import PWMOut

# The delay on the PWM cycles. Increase to slow down the LED pulsing, decrease to speed it up.
delay = 0.01

# For most boards.
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

# For the QT Py RP2040, QT Py ESP32-S2, other boards that have SCL1/SDA1 as the STEMMA QT port.
# import busio
# i2c = busio.I2C(board.SCL1, board.SDA1)
arcade_qt = Seesaw(i2c, addr=0x3A)

# Button pins in order (1, 2, 3, 4)
button_pins = (18, 19, 20, 2)
buttons = []
for button_pin in button_pins:
    button = DigitalIO(arcade_qt, button_pin)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP
    buttons.append(button)

# LED pins in order (1, 2, 3, 4)
led_pins = (12, 13, 0, 1)
leds = []
for led_pin in led_pins:
    led = PWMOut(arcade_qt, led_pin)
    leds.append(led)

while True:
    for led_number, button in enumerate(buttons):
        if not button.value:
            for cycle in range(0, 65535, 8000):
                leds[led_number].duty_cycle = cycle
                time.sleep(delay)
            for cycle in range(65534, 0, -8000):
                leds[led_number].duty_cycle = cycle
                time.sleep(delay)
