# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""
Display an image on the LCD, then record an image when the REC button is pressed/held.

The Kaluga development kit comes in two versions (v1.2 and v1.3); this demo is
tested on v1.3.

The audio board must be mounted between the Kaluga and the LCD, it provides the
I2C pull-ups(!)

The v1.3 development kit's LCD can have one of two chips, the ili9341 or
st7789.  Furthermore, there are at least 2 ILI9341 variants, one of which needs
rotation=90!  This demo is for the ili9341.  If the display is garbled, try adding
rotation=90, or try modifying it to use ST7799.

This example also requires an SD card breakout wired as follows:
 * IO18: SD Clock Input
 * IO17: SD Serial Output (MISO)
 * IO14: SD Serial Input (MOSI)
 * IO12: SD Chip Select

Insert a CircuitPython-compatible SD card before powering on the Kaluga.
Press the "Record" button on the audio daughterboard to take a photo.
"""

import os

import analogio
import board
import busio
import displayio
import sdcardio
import storage
from adafruit_ili9341 import ILI9341
import adafruit_ov2640

V_MODE = 1.98
V_RECORD = 2.41

a = analogio.AnalogIn(board.IO6)

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

sd_spi = busio.SPI(clock=board.IO18, MOSI=board.IO14, MISO=board.IO17)
sd_cs = board.IO12
sdcard = sdcardio.SDCard(sd_spi, sd_cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")


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
        cam.size = adafruit_ov2640.OV2640_SIZE_UXGA
        cam.colorspace = adafruit_ov2640.OV2640_COLOR_JPEG
        b = bytearray(cam.capture_buffer_size)
        jpeg = cam.capture(b)

        print(f"Captured {len(jpeg)} bytes of jpeg data")
        with open_next_image() as f:
            f.write(jpeg)
    finally:
        cam.size = old_size
        cam.colorspace = old_colorspace


display.auto_refresh = False
while True:
    a_voltage = a.value * a.reference_voltage / 65535  # pylint: disable=no-member
    record_pressed = abs(a_voltage - V_RECORD) < 0.05
    if record_pressed:
        capture_image()
    cam.capture(bitmap)
    bitmap.dirty()
    display.refresh(minimum_frames_per_second=0)
