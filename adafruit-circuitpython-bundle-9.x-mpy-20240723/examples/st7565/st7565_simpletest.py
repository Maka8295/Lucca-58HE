# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-FileCopyrightText: 2021 Mark Olsson <mark@markolsson.se>
# SPDX-License-Identifier: MIT

import time
import board
import busio
import digitalio

import adafruit_st7565

# Initialize SPI bus and control pins
spi = busio.SPI(board.SCK, MOSI=board.MOSI)
dc = digitalio.DigitalInOut(board.D5)  # data/command
cs = digitalio.DigitalInOut(board.D6)  # Chip select
reset = digitalio.DigitalInOut(board.D9)  # reset

display = adafruit_st7565.ST7565(spi, dc, cs, reset)

display.contrast = 0

# Turn on the Backlight LED
backlight = digitalio.DigitalInOut(board.D10)  # backlight
backlight.switch_to_output()
backlight.value = True

print("Pixel test")
# Clear the display.  Always call show after changing pixels to make the display
# update visible!
display.fill(0)
display.show()

# Set a pixel in the origin 0,0 position.
display.pixel(0, 0, 1)
# Set a pixel in the middle position.
display.pixel(display.width // 2, display.height // 2, 1)
# Set a pixel in the opposite corner position.
display.pixel(display.width - 1, display.height - 1, 1)
display.show()
time.sleep(2)

print("Lines test")
# we'll draw from corner to corner, lets define all the pair coordinates here
corners = (
    (0, 0),
    (0, display.height - 1),
    (display.width - 1, 0),
    (display.width - 1, display.height - 1),
)

display.fill(0)
for corner_from in corners:
    for corner_to in corners:
        display.line(corner_from[0], corner_from[1], corner_to[0], corner_to[1], 1)
display.show()
time.sleep(2)

print("Rectangle test")
display.fill(0)
w_delta = display.width / 10
h_delta = display.height / 10
for i in range(11):
    display.rect(0, 0, int(w_delta * i), int(h_delta * i), 1)
display.show()
time.sleep(2)

print("Text test")
display.fill(0)
display.text("hello world", 0, 0, 1)
display.text("this is the", 0, 8, 1)
display.text("CircuitPython", 0, 16, 1)
display.text("adafruit lib-", 0, 24, 1)
display.text("rary for the", 0, 32, 1)
display.text("ST7565! :) ", 0, 40, 1)

display.show()

while True:
    display.invert = True
    time.sleep(0.5)
    display.invert = False
    time.sleep(0.5)
