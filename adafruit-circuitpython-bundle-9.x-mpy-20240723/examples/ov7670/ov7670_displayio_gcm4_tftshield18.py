# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time
import board
import busio
import digitalio
import displayio
from adafruit_seesaw.tftshield18 import TFTShield18
from adafruit_st7735r import ST7735R
from adafruit_ov7670 import (  # pylint: disable=unused-import
    OV7670,
    OV7670_TEST_PATTERN_COLOR_BAR,
    OV7670_SIZE_DIV4,
    OV7670_SIZE_DIV8,
    OV7670_NIGHT_MODE_2,
)

# Pylint is unable to see that the "size" property of OV7670_GrandCentral exists
# pylint: disable=attribute-defined-outside-init

# Release any resources currently in use for the displays
displayio.release_displays()

ss = TFTShield18()

spi = board.SPI()
tft_cs = board.D10
tft_dc = board.D8

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)

ss.tft_reset()
display = ST7735R(
    display_bus, width=160, height=128, rotation=90, bgr=True, auto_refresh=False
)

ss.set_backlight(True)


class OV7670_GrandCentral(OV7670):
    def __init__(self):
        with digitalio.DigitalInOut(board.D39) as shutdown:
            shutdown.switch_to_output(True)
            time.sleep(0.001)
            bus = busio.I2C(board.D24, board.D25)
        self._bus = bus
        OV7670.__init__(
            self,
            bus,
            mclk=board.PCC_XCLK,
            data_pins=[
                board.PCC_D0,
                board.PCC_D1,
                board.PCC_D2,
                board.PCC_D3,
                board.PCC_D4,
                board.PCC_D5,
                board.PCC_D6,
                board.PCC_D7,
            ],
            clock=board.PCC_CLK,
            vsync=board.PCC_DEN1,
            href=board.PCC_DEN2,
            shutdown=board.D39,
            reset=board.D38,
        )

    def deinit(self):
        self._bus.deinit()
        OV7670.deinit(self)


cam = OV7670_GrandCentral()

cam.size = OV7670_SIZE_DIV4
cam.flip_x = False
cam.flip_y = True
pid = cam.product_id
ver = cam.product_version
print(f"Detected pid={pid:x} ver={ver:x}")
# cam.test_pattern = OV7670_TEST_PATTERN_COLOR_BAR

g = displayio.Group(scale=1)
bitmap = displayio.Bitmap(160, 120, 65536)
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
