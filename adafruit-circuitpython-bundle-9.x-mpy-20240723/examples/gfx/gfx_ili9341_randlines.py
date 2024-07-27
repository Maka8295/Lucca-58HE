# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Random line drawing with ILI9341 TFT display.
# This is made to work with ESP8266 MicroPython and the TFT FeatherWing, but
# adjust the SPI and display initialization at the start to change boards.
# Author: Tony DiCola
# License: MIT License (https://opensource.org/licenses/MIT)
import time
import gfx
import ili9341
import machine
import uos


def randrange(min_value, max_value):
    # Simple randrange implementation for ESP8266 uos.urandom function.
    # Returns a random integer in the range min to max.  Supports only 32-bit
    # int values at most.
    magnitude = abs(max_value - min_value)
    randbytes = uos.urandom(4)
    offset = int(
        (randbytes[3] << 24) | (randbytes[2] << 16) | (randbytes[1] << 8) | randbytes[0]
    )
    offset %= magnitude + 1  # Offset by one to allow max_value to be included.
    return min_value + offset


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

# Now loop forever drawing random lines.
display.fill(0)
while True:
    x0 = randrange(0, 240)
    y0 = randrange(0, 320)
    x1 = randrange(0, 240)
    y1 = randrange(0, 320)
    r = randrange(0, 255)
    g = randrange(0, 255)
    b = randrange(0, 255)
    graphics.line(x0, y0, x1, y1, ili9341.color565(r, g, b))
    time.sleep(0.01)
