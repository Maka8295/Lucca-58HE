# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Quick bitmap test of RA8875 with Feather M4
import struct

import busio
import digitalio
import board

from adafruit_ra8875 import ra8875
from adafruit_ra8875.ra8875 import color565

WHITE = color565(255, 255, 255)

# Configuration for CS and RST pins:
cs_pin = digitalio.DigitalInOut(board.D9)
rst_pin = digitalio.DigitalInOut(board.D10)

# Config for display baudrate (default max is 6mhz):
BAUDRATE = 8000000

# Setup SPI bus using hardware SPI:
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Create and setup the RA8875 display:
display = ra8875.RA8875(spi, cs=cs_pin, rst=rst_pin, baudrate=BAUDRATE)
display.init()
display.fill(WHITE)


def convert_555_to_565(rgb):
    return (rgb & 0x7FE0) << 1 | 0x20 | rgb & 0x001F


class BMP:
    def __init__(self, filename):
        self.filename = filename
        self.colors = None
        self.data = 0
        self.data_size = 0
        self.bpp = 0
        self.width = 0
        self.height = 0
        self.read_header()

    def read_header(self):
        if self.colors:
            return
        with open(self.filename, "rb") as f:
            f.seek(10)
            self.data = int.from_bytes(f.read(4), "little")
            f.seek(18)
            self.width = int.from_bytes(f.read(4), "little")
            self.height = int.from_bytes(f.read(4), "little")
            f.seek(28)
            self.bpp = int.from_bytes(f.read(2), "little")
            f.seek(34)
            self.data_size = int.from_bytes(f.read(4), "little")
            f.seek(46)
            self.colors = int.from_bytes(f.read(4), "little")

    def draw(self, disp, x=0, y=0):
        print("{:d}x{:d} image".format(self.width, self.height))
        print("{:d}-bit encoding detected".format(self.bpp))
        line = 0
        line_size = self.width * (self.bpp // 8)
        if line_size % 4 != 0:
            line_size += 4 - line_size % 4
        current_line_data = b""
        with open(self.filename, "rb") as f:
            f.seek(self.data)
            disp.set_window(x, y, self.width, self.height)
            for line in range(self.height):
                current_line_data = b""
                line_data = f.read(line_size)
                for i in range(0, line_size, self.bpp // 8):
                    if (line_size - i) < self.bpp // 8:
                        break
                    if self.bpp == 16:
                        color = convert_555_to_565(line_data[i] | line_data[i + 1] << 8)
                    if self.bpp in (24, 32):
                        color = color565(
                            line_data[i + 2], line_data[i + 1], line_data[i]
                        )
                    current_line_data = current_line_data + struct.pack(">H", color)
                disp.setxy(x, self.height - line + y)
                disp.push_pixels(current_line_data)
            disp.set_window(0, 0, disp.width, disp.height)


bitmap = BMP("/ra8875_blinka.bmp")
x_position = (display.width // 2) - (bitmap.width // 2)
y_position = (display.height // 2) - (bitmap.height // 2)
bitmap.draw(display, x_position, y_position)
