# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Simple painting demo that draws on an Adafruit capacitive touch shield with
ILI9341 display and STMPE610 resistive touch driver
"""

import busio
import board
import digitalio
from adafruit_rgb_display import ili9341, color565
import adafruit_stmpe610

# Create library object using our Bus SPI port
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Adafruit Metro M0 + 2.8" Capacitive touch shield
cs_pin = digitalio.DigitalInOut(board.D9)
dc_pin = digitalio.DigitalInOut(board.D10)

# Initialize display
display = ili9341.ILI9341(spi, cs=cs_pin, dc=dc_pin)
# Fill with black!
display.fill(color565(0, 0, 0))

st_cs_pin = digitalio.DigitalInOut(board.D6)
st = adafruit_stmpe610.Adafruit_STMPE610_SPI(spi, st_cs_pin)

while True:
    if st.touched:
        while not st.buffer_empty:
            ts = st.touches
            for point in ts:
                # perform transformation to get into display coordinate system!
                y = point["y"]
                x = 4096 - point["x"]
                x = 2 * x // 30
                y = 8 * y // 90
                display.fill_rectangle(x - 2, y - 2, 4, 4, color565(255, 0, 0))
