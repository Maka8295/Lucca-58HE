# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test of primitive drawing with ILI9341 TFT display.
# This is made to work with ESP8266 MicroPython and the TFT FeatherWing, but
# adjust the SPI and display initialization at the start to change boards.
# Author: Tony DiCola
# License: MIT License (https://opensource.org/licenses/MIT)
import time
import gfx
import ili9341
import machine


# Setup hardware SPI at 32mhz on ESP8266 MicroPython.
spi = machine.SPI(1, baudrate=32000000)

# Setup ILI9341 display using TFT FeatherWing pinout for CS & DC pins.
display = ili9341.ILI9341(spi, cs=machine.Pin(0), dc=machine.Pin(15))


# Optionally create faster horizontal and vertical line drawing functions using
# the display's native filled rectangle function (which updates chunks of memory
# instead of pixel by pixel).
def fast_hline(x, y, width, color):
    display.fill_rectangle(x, y, width, 1, color)


def fast_vline(x, y, height, color):
    display.fill_rectangle(x, y, 1, height, color)


# Initialize the GFX library, giving it the display pixel function as its pixel
# drawing primitive command.  The hline and vline parameters specify optional
# optimized horizontal and vertical line drawing functions.  You can remove these
# to see how much slower the filled shape functions perform!
graphics = gfx.GFX(240, 320, display.pixel, hline=fast_hline, vline=fast_vline)

# Now loop forever drawing different primitives.
while True:
    # Clear screen and draw a red line.
    display.fill(0)
    graphics.line(0, 0, 239, 319, ili9341.color565(255, 0, 0))
    time.sleep(2)
    # Clear screen and draw a green rectangle.
    display.fill(0)
    graphics.rect(0, 0, 120, 160, ili9341.color565(0, 255, 0))
    time.sleep(2)
    # Clear screen and draw a filled green rectangle.
    display.fill(0)
    graphics.fill_rect(0, 0, 120, 160, ili9341.color565(0, 255, 0))
    time.sleep(2)
    # Clear screen and draw a blue circle.
    display.fill(0)
    graphics.circle(120, 160, 60, ili9341.color565(0, 0, 255))
    time.sleep(2)
    # Clear screen and draw a filled blue circle.
    display.fill(0)
    graphics.fill_circle(120, 160, 60, ili9341.color565(0, 0, 255))
    time.sleep(2)
    # Clear screen and draw a pink triangle.
    display.fill(0)
    graphics.triangle(120, 100, 180, 160, 60, 160, ili9341.color565(255, 0, 255))
    time.sleep(2)
    # Clear screen and draw a filled pink triangle.
    display.fill(0)
    graphics.fill_triangle(120, 100, 180, 160, 60, 160, ili9341.color565(255, 0, 255))
    time.sleep(2)
