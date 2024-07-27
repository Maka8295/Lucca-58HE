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

import board
import busio
import displayio
from adafruit_ili9341 import ILI9341
import ulab.numpy as np
import adafruit_ov2640

# Pylint is unable to see that the "size" property of OV2640_GrandCentral exists
# pylint: disable=attribute-defined-outside-init

# Release any resources currently in use for the displays
displayio.release_displays()

spi = busio.SPI(MOSI=board.LCD_MOSI, clock=board.LCD_CLK)
display_bus = displayio.FourWire(
    spi, command=board.LCD_D_C, chip_select=board.LCD_CS, reset=board.LCD_RST
)
display = ILI9341(display_bus, width=320, height=240, rotation=90)

bus = busio.I2C(scl=board.CAMERA_SIOC, sda=board.CAMERA_SIOD)
cam = adafruit_ov2640.OV2640(
    bus,
    data_pins=board.CAMERA_DATA,
    clock=board.CAMERA_PCLK,
    vsync=board.CAMERA_VSYNC,
    href=board.CAMERA_HREF,
    mclk=board.CAMERA_XCLK,
    mclk_frequency=20_000_000,
    size=adafruit_ov2640.OV2640_SIZE_QVGA,
)

cam.flip_x = False
cam.flip_y = True
pid = cam.product_id
ver = cam.product_version
print(f"Detected pid={pid:x} ver={ver:x}")
cam.test_pattern = True

g = displayio.Group(scale=1)
bitmap = displayio.Bitmap(320, 240, 65536)
arr = np.frombuffer(bitmap, dtype=np.uint16)
tg = displayio.TileGrid(
    bitmap,
    pixel_shader=displayio.ColorConverter(
        input_colorspace=displayio.Colorspace.RGB565_SWAPPED
    ),
)
g.append(tg)
display.root_group = g

display.auto_refresh = False
while True:
    cam.capture(bitmap)
    arr[:] = ~arr  # Invert every pixel in the bitmap, via the array
    bitmap.dirty()
    display.refresh(minimum_frames_per_second=0)

cam.deinit()
