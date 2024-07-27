# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import displayio
import adafruit_ssd1327

displayio.release_displays()

# Use for I2C
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
display_bus = displayio.I2CDisplay(i2c, device_address=0x3D)

# Use for SPI
# spi = board.SPI()
# oled_cs = board.D5
# oled_dc = board.D6
# display_bus = displayio.FourWire(
#    spi, command=oled_dc, chip_select=oled_cs, baudrate=1000000, reset=board.D9
# )


time.sleep(1)
display = adafruit_ssd1327.SSD1327(display_bus, width=128, height=128)

g = displayio.Group()
dimension = min(display.width, display.height)
color_count = 16
gamma_pattern = displayio.Bitmap(dimension, dimension, color_count)
gamma_palette = displayio.Palette(color_count)
t = displayio.TileGrid(gamma_pattern, pixel_shader=gamma_palette)

pixels_per_step = dimension // color_count

for i in range(dimension):
    if i % pixels_per_step == 0:
        continue
    gamma_pattern[i, i] = i // pixels_per_step

for i in range(color_count):
    component = i * 255 // (color_count - 1)
    print(component)
    gamma_palette[i] = component << 16 | component << 8 | component

g.append(t)

display.root_group = g

time.sleep(10)
