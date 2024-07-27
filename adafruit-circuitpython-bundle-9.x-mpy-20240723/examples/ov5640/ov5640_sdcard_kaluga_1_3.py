# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""
The Kaluga development kit comes in two versions (v1.2 and v1.3); this demo is
tested on v1.3.

The audio board must be mounted between the Kaluga and the LCD, it provides the
I2C pull-ups(!)

This example also requires an SD card breakout wired as follows:
 * IO18: SD Clock Input
 * IO17: SD Serial Output (MISO)
 * IO14: SD Serial Input (MOSI)
 * IO12: SD Chip Select

Insert a CircuitPython-compatible SD card before powering on the Kaluga.
Press the "Record" button on the audio daughterboard to take a photo.
"""

import os
import time

import analogio
import board
import busio
import displayio
import neopixel
import sdcardio
import storage

import adafruit_ili9341
import adafruit_ov5640

# Release any resources currently in use for the displays
displayio.release_displays()
spi = busio.SPI(MOSI=board.LCD_MOSI, clock=board.LCD_CLK)
display_bus = displayio.FourWire(
    spi,
    command=board.LCD_D_C,
    chip_select=board.LCD_CS,
    reset=board.LCD_RST,
    baudrate=80_000_000,
)
display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240, rotation=90)

V_MODE = 1.98
V_RECORD = 2.41

a = analogio.AnalogIn(board.IO6)

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.3, auto_write=False)

bus = busio.I2C(scl=board.CAMERA_SIOC, sda=board.CAMERA_SIOD)
cam = adafruit_ov5640.OV5640(
    bus,
    data_pins=board.CAMERA_DATA,
    clock=board.CAMERA_PCLK,
    vsync=board.CAMERA_VSYNC,
    href=board.CAMERA_HREF,
    mclk=board.CAMERA_XCLK,
    size=adafruit_ov5640.OV5640_SIZE_QSXGA,
)

sd_spi = busio.SPI(clock=board.IO18, MOSI=board.IO14, MISO=board.IO17)
sd_cs = board.IO12
sdcard = sdcardio.SDCard(sd_spi, sd_cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")


def exists(filename):
    try:
        os.stat(filename)
        return True
    except OSError as _:
        return False


_image_counter = 0


def open_next_image():
    global _image_counter  # pylint: disable=global-statement
    while True:
        filename = f"/sd/img{_image_counter:04d}.jpg"
        _image_counter += 1
        if exists(filename):
            continue
        print("# writing to", filename)
        return open(filename, "wb")


cam.colorspace = adafruit_ov5640.OV5640_COLOR_JPEG
cam.quality = 7
b = bytearray(cam.capture_buffer_size)

print("Press 'record' button to take a JPEG image")
while True:
    pixel[0] = 0x0000FF
    pixel.write()
    a_voltage = a.value * a.reference_voltage / 65535  # pylint: disable=no-member
    record_pressed = abs(a_voltage - V_RECORD) < 0.05
    if record_pressed:
        pixel[0] = 0xFF0000
        pixel.write()
        time.sleep(0.01)
        jpeg = cam.capture(b)
        print(
            f"Captured {len(jpeg)} bytes of jpeg data"
            f" (had allocated {cam.capture_buffer_size} bytes"
        )
        print(f"Resolution {cam.width}x{cam.height}")
        try:
            pixel[0] = 0x00FF00
            pixel.write()
            with open_next_image() as f:
                f.write(jpeg)
            print("# Wrote image")
            pixel[0] = 0x000000
            pixel.write()
        except OSError as e:
            print(e)
        while record_pressed:
            a_voltage = (
                a.value * a.reference_voltage / 65535
            )  # pylint: disable=no-member
            record_pressed = abs(a_voltage - V_RECORD) < 0.05
