# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
import digitalio

import adafruit_sharpmemorydisplay

# Initialize SPI bus and control pins
spi = busio.SPI(board.SCK, MOSI=board.MOSI)
scs = digitalio.DigitalInOut(board.D6)  # inverted chip select

# pass in the display size, width and height, as well
# display = adafruit_sharpmemorydisplay.SharpMemoryDisplay(spi, scs, 96, 96)
display = adafruit_sharpmemorydisplay.SharpMemoryDisplay(spi, scs, 144, 168)

print("Pixel test")

# Clear the display.  Always call show after changing pixels to make the display
# update visible!
display.fill(1)
display.show()

# Set a pixel in the origin 0,0 position.
display.pixel(0, 0, 0)
# Set a pixel in the middle position.
display.pixel(display.width // 2, display.width // 2, 0)
# Set a pixel in the opposite corner position.
display.pixel(display.width - 1, display.height - 1, 0)
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

display.fill(1)
for corner_from in corners:
    for corner_to in corners:
        display.line(corner_from[0], corner_from[1], corner_to[0], corner_to[1], 0)
display.show()
time.sleep(2)

print("Rectangle test")
display.fill(1)
w_delta = display.width / 10
h_delta = display.height / 10
for i in range(11):
    display.rect(0, 0, int(w_delta * i), int(h_delta * i), 0)
display.show()
time.sleep(2)

print("Text test")
display.fill(1)
display.text(" hello world!", 0, 0, 0)
display.text(" This is the", 0, 8, 0)
display.text(" CircuitPython", 0, 16, 0)
display.text("adafruit library", 0, 24, 0)
display.text(" for the SHARP", 0, 32, 0)
display.text(" Memory Display :) ", 0, 40, 0)
display.show()
