# SPDX-FileCopyrightText: Copyright (c) 2024 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense


import board
import displayio
from adafruit_hx8357 import HX8357
import adafruit_tsc2007

# Initialize the Display
displayio.release_displays()

spi = board.SPI()
tft_cs = board.D9
tft_dc = board.D10

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = HX8357(display_bus, width=480, height=320)

# Use for I2C
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

tsc = adafruit_tsc2007.TSC2007(i2c, invert_x=True, swap_xy=True)

while True:
    if tsc.touched:
        point = tsc.touch
        if point["pressure"] < 100:  # ignore touches with no 'pressure' as false
            continue
        print("Touchpoint: (%d, %d, %d)" % (point["x"], point["y"], point["pressure"]))
