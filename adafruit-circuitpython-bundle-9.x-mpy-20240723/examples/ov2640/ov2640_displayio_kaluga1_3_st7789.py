# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""
The Kaluga development kit comes in two versions (v1.2 and v1.3); this demo is
tested on v1.3.

The v1.3 development kit's LCD can have one of two chips, the ili9341 or
st7789.  This demo is for the ili9341.  There is no marking to distinguish the
two chips.  If the visible portion of the display's flexible cable has a bunch
of straight lines, it may be an ili9341.  If it has a bunch of wiggly traces,
it may be an st7789.  If in doubt, try both demos.

The audio board must be mounted between the Kaluga and the LCD, it provides the
I2C pull-ups(!)
"""

import board
import busio
import displayio
from adafruit_st7789 import ST7789
import adafruit_ov2640

# Pylint is unable to see that the "size" property of OV2640_GrandCentral exists
# pylint: disable=attribute-defined-outside-init

# Release any resources currently in use for the displays
displayio.release_displays()

spi = busio.SPI(MOSI=board.LCD_MOSI, clock=board.LCD_CLK)
display_bus = displayio.FourWire(
    spi, command=board.LCD_D_C, chip_select=board.LCD_CS, reset=board.LCD_RST
)
display = ST7789(
    display_bus, width=320, height=240, rotation=90, reverse_bytes_in_word=True
)

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

# cam.flip_x = False
# cam.flip_y = True
pid = cam.product_id
ver = cam.product_version
print(f"Detected pid={pid:x} ver={ver:x}")
# cam.test_pattern = True

g = displayio.Group(scale=1)
bitmap = displayio.Bitmap(320, 240, 65536)
tg = displayio.TileGrid(
    bitmap,
    pixel_shader=displayio.ColorConverter(
        input_colorspace=displayio.Colorspace.BGR565_SWAPPED
    ),
)
g.append(tg)
display.root_group = g

display.auto_refresh = False
while True:
    cam.capture(bitmap)
    bitmap.dirty()
    display.refresh(minimum_frames_per_second=0)
    print(".")

cam.deinit()
