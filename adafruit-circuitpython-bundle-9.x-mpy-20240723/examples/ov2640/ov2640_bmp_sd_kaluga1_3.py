# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""
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
Press the "Record" button on the audio daughterboard to take a photo in BMP format.
"""

import os
import struct
import ulab.numpy as np

import analogio
import board
import busio
import displayio
import sdcardio
import storage
import adafruit_ov2640

# Nominal voltages of several of the buttons on the audio daughterboard
V_MODE = 1.98
V_RECORD = 2.41

a = analogio.AnalogIn(board.IO6)

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
_INIT_SEQUENCE = (
    b"\x01\x80\x80"  # Software reset then delay 0x80 (128ms)
    b"\xEF\x03\x03\x80\x02"
    b"\xCF\x03\x00\xC1\x30"
    b"\xED\x04\x64\x03\x12\x81"
    b"\xE8\x03\x85\x00\x78"
    b"\xCB\x05\x39\x2C\x00\x34\x02"
    b"\xF7\x01\x20"
    b"\xEA\x02\x00\x00"
    b"\xc0\x01\x23"  # Power control VRH[5:0]
    b"\xc1\x01\x10"  # Power control SAP[2:0];BT[3:0]
    b"\xc5\x02\x3e\x28"  # VCM control
    b"\xc7\x01\x86"  # VCM control2
    b"\x36\x01\x90"  # Memory Access Control
    b"\x37\x01\x00"  # Vertical scroll zero
    b"\x3a\x01\x55"  # COLMOD: Pixel Format Set
    b"\xb1\x02\x00\x18"  # Frame Rate Control (In Normal Mode/Full Colors)
    b"\xb6\x03\x08\x82\x27"  # Display Function Control
    b"\xF2\x01\x00"  # 3Gamma Function Disable
    b"\x26\x01\x01"  # Gamma curve selected
    b"\xe0\x0f\x0F\x31\x2B\x0C\x0E\x08\x4E\xF1\x37\x07\x10\x03\x0E\x09\x00"  # Set Gamma
    b"\xe1\x0f\x00\x0E\x14\x03\x11\x07\x31\xC1\x48\x08\x0F\x0C\x31\x36\x0F"  # Set Gamma
    b"\x11\x80\x78"  # Exit Sleep then delay 0x78 (120ms)
    b"\x29\x80\x78"  # Display on then delay 0x78 (120ms)
)

display = displayio.Display(
    display_bus, _INIT_SEQUENCE, width=320, height=240, auto_refresh=False
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

cam.flip_x = False
cam.flip_y = False
cam.test_pattern = False

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


def open_next_image(extension="jpg"):
    global _image_counter  # pylint: disable=global-statement
    while True:
        filename = f"/sd/img{_image_counter:04d}.{extension}"
        _image_counter += 1
        if exists(filename):
            continue
        print("#", filename)
        return open(filename, "wb")  # pylint: disable=consider-using-with


### These routines are for writing BMP files in the RGB565 or BGR565 formats.
_BI_BITFIELDS = 3

_bitmask_rgb565 = (0xF800, 0x7E0, 0x1F)
_bitmask_bgr565 = (0x1F, 0x7E0, 0xF800)


def write_header(output_file, width, height, masks):
    def put_word(value):
        output_file.write(struct.pack("<H", value))

    def put_dword(value):
        output_file.write(struct.pack("<I", value))

    def put_long(value):
        output_file.write(struct.pack("<i", value))

    def put_padding(length):
        output_file.write(b"\0" * length)

    filesize = 14 + 108 + height * width * 2

    # BMP header
    output_file.write(b"BM")
    put_dword(filesize)
    put_word(0)  # Creator 1
    put_word(0)  # Creator 2
    put_dword(14 + 108)  # Offset of bitmap data

    # DIB header (BITMAPV4HEADER)
    put_dword(108)  # sizeof(BITMAPV4HEADER)
    put_long(width)
    put_long(-height)
    put_word(1)  # number of color planes (must be 1)
    put_word(16)  # number of bits per pixel
    put_dword(_BI_BITFIELDS)  # "compression"
    put_dword(2 * width * height)  # size of raw bitmap data
    put_long(11811)  # 72dpi -> pixels/meter
    put_long(11811)  # 72dpi -> pixels/meter
    put_dword(0)  # palette size
    put_dword(0)  # important color count
    put_dword(masks[0])  # red mask
    put_dword(masks[1])  # green mask
    put_dword(masks[2])  # blue mask
    put_dword(0)  # alpha mask
    put_dword(0)  # CS Type
    put_padding(3 * 3 * 4)  # CIEXYZ infrmation
    put_dword(144179)  # 2.2 gamma red
    put_dword(144179)  # 2.2 gamma green
    put_dword(144179)  # 2.2 gamma blue


def capture_image_bmp(the_bitmap):
    with open_next_image("bmp") as f:
        swapped = np.frombuffer(the_bitmap, dtype=np.uint16)
        swapped.byteswap(inplace=True)
        write_header(f, the_bitmap.width, the_bitmap.height, _bitmask_rgb565)
        f.write(swapped)


display.auto_refresh = False
old_record_pressed = True

while True:
    a_voltage = a.value * a.reference_voltage / 65535  # pylint: disable=no-member
    cam.capture(bitmap)
    bitmap.dirty()

    record_pressed = abs(a_voltage - V_RECORD) < 0.05
    display.refresh(minimum_frames_per_second=0)
    if record_pressed and not old_record_pressed:
        capture_image_bmp(bitmap)
    old_record_pressed = record_pressed
