# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""
The Kaluga development kit comes in two versions (v1.2 and v1.3); this demo is
tested on v1.3.  It probably won't work on v1.2 without modification.

The v1.3 development kit's LCD can have one of two chips, the ili9341 or
st7789.  Furthermore, there are at least 2 ILI9341 variants, one of which needs
rotation=90!  This demo is for the ili9341.  If the display is garbled, try adding
rotation=90, or try modifying it to use ST7799.

The camera included with the Kaluga development kit is the incompatible OV2640,
it won't work.

The audio board must be mounted between the Kaluga and the LCD, it provides the
I2C pull-ups(!)
"""

import time
import board
import busio
import displayio
from adafruit_ili9341 import ILI9341
from adafruit_ov7670 import (  # pylint: disable=unused-import
    OV7670,
    OV7670_TEST_PATTERN_COLOR_BAR,
    OV7670_SIZE_DIV2,
    OV7670_NIGHT_MODE_2,
)

# Pylint is unable to see that the "size" property of OV7670_GrandCentral exists
# pylint: disable=attribute-defined-outside-init

# Release any resources currently in use for the displays
displayio.release_displays()

spi = busio.SPI(MOSI=board.LCD_MOSI, clock=board.LCD_CLK)
display_bus = displayio.FourWire(
    spi, command=board.LCD_D_C, chip_select=board.LCD_CS, reset=board.LCD_RST
)
display = ILI9341(display_bus, width=320, height=240)

bus = busio.I2C(scl=board.CAMERA_SIOC, sda=board.CAMERA_SIOD)
cam = OV7670(
    bus,
    data_pins=board.CAMERA_DATA,
    clock=board.CAMERA_PCLK,
    vsync=board.CAMERA_VSYNC,
    href=board.CAMERA_HREF,
    mclk=board.CAMERA_XCLK,
    mclk_frequency=20_000_000,
)

cam.size = OV7670_SIZE_DIV2
cam.flip_x = False
cam.flip_y = True
pid = cam.product_id
ver = cam.product_version
print(f"Detected pid={pid:x} ver={ver:x}")
# cam.test_pattern = OV7670_TEST_PATTERN_COLOR_BAR

g = displayio.Group(scale=1)
bitmap = displayio.Bitmap(320, 240, 65536)
tg = displayio.TileGrid(
    bitmap,
    pixel_shader=displayio.ColorConverter(
        input_colorspace=displayio.Colorspace.RGB565_SWAPPED
    ),
)
g.append(tg)
display.root_group = g

t0 = time.monotonic_ns()
display.auto_refresh = False
while True:
    cam.capture(bitmap)
    bitmap.dirty()
    display.refresh(minimum_frames_per_second=0)
    t1 = time.monotonic_ns()
    print("fps", 1e9 / (t1 - t0))
    t0 = t1

cam.deinit()
