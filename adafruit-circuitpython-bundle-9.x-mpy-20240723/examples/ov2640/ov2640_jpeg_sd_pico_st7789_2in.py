# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""
Display an image on the LCD, then record an image when a button is pressed/held.

Uses the SD Card present on the 2inch st7789 breakout board

This example also requires an SD card breakout wired as follows:
SPI BUS - same as the ST7789 -- with MISO connected
 * GP2: SD Clock Input
 * GP3: SD Serial Input (MOSI)
 * GP4: SD Serial Output (MISO)
 * GP5: SD Chip Select

A button is needed to trigger the capture
Attach a button to  GROUND and GP22

Insert a CircuitPython-compatible SD card before powering on the Kaluga.
Press the "Record" button on the audio daughterboard to take a photo.
"""

import time
import os
from displayio import (
    Bitmap,
    Group,
    TileGrid,
    FourWire,
    release_displays,
    ColorConverter,
    Colorspace,
)
from adafruit_st7789 import ST7789
import board
import busio
import digitalio
import sdcardio
import storage
import adafruit_ov2640

release_displays()
# Set up the display (You must customize this block for your display!)
spi = busio.SPI(clock=board.GP2, MOSI=board.GP3, MISO=board.GP4)
# setup the SD Card
sd_cs = board.GP5
sdcard = sdcardio.SDCard(spi, sd_cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")
# setup the button
button = digitalio.DigitalInOut(board.GP22)
button.pull = digitalio.Pull.UP

display_bus = FourWire(spi, command=board.GP0, chip_select=board.GP1, reset=None)
display = ST7789(display_bus, width=320, height=240, rotation=270)
display.auto_refresh = False

# Ensure the camera is shut down, so that it releases the SDA/SCL lines,
# then create the configuration I2C bus

with digitalio.DigitalInOut(board.GP10) as reset:
    reset.switch_to_output(False)
    time.sleep(0.001)
    bus = busio.I2C(board.GP9, board.GP8)

# Set up the camera (you must customize this for your board!)
cam = adafruit_ov2640.OV2640(
    bus,
    data_pins=[
        board.GP12,
        board.GP13,
        board.GP14,
        board.GP15,
        board.GP16,
        board.GP17,
        board.GP18,
        board.GP19,
    ],  # [16]     [org] etc
    clock=board.GP11,  # [15]     [blk]
    vsync=board.GP7,  # [10]     [brn]
    href=board.GP21,  # [27/o14] [red]
    mclk=board.GP20,  # [16/o15]
    shutdown=None,
    reset=board.GP10,
)  # [14]

width = display.width
height = display.height

cam.size = adafruit_ov2640.OV2640_SIZE_QQVGA
# cam.test_pattern = True
bitmap = Bitmap(cam.width, cam.height, 65536)

print(width, height, cam.width, cam.height)
if bitmap is None:
    raise SystemExit("Could not allocate a bitmap")

g = Group(scale=1, x=(width - cam.width) // 2, y=(height - cam.height) // 2)
tg = TileGrid(
    bitmap, pixel_shader=ColorConverter(input_colorspace=Colorspace.RGB565_SWAPPED)
)
g.append(tg)
display.root_group = g

display.auto_refresh = False


def exists(filename):
    try:
        os.stat(filename)
        return True
    except OSError:
        return False


_image_counter = 0


def open_next_image():
    global _image_counter  # pylint: disable=global-statement
    while True:
        filename = f"/sd/img{_image_counter:04d}.jpg"
        _image_counter += 1
        if exists(filename):
            continue
        print("#", filename)
        return open(filename, "wb")  # pylint: disable=consider-using-with


def capture_image():
    old_size = cam.size
    old_colorspace = cam.colorspace

    try:
        cam.size = adafruit_ov2640.OV2640_SIZE_QVGA
        cam.colorspace = adafruit_ov2640.OV2640_COLOR_JPEG
        b = bytearray(cam.capture_buffer_size)
        jpeg = cam.capture(b)

        print(f"Captured {len(jpeg)} bytes of jpeg data")
        with open_next_image() as f:
            f.write(jpeg)
    finally:
        cam.size = old_size
        cam.colorspace = old_colorspace


def main():
    display.auto_refresh = False
    while True:
        if not button.value:  # button pressed
            capture_image()
        cam.capture(bitmap)
        bitmap.dirty()
        display.refresh(minimum_frames_per_second=0)


main()
