# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import os
import fcntl
import mmap
import struct
import digitalio
import board
from PIL import Image, ImageDraw
from adafruit_rgb_display import st7789

# definitions from linux/fb.h
FBIOGET_VSCREENINFO = 0x4600
FBIOGET_FSCREENINFO = 0x4602
FBIOBLANK = 0x4611

FB_TYPE_PACKED_PIXELS = 0
FB_TYPE_PLANES = 1
FB_TYPE_INTERLEAVED_PLANES = 2
FB_TYPE_TEXT = 3
FB_TYPE_VGA_PLANES = 4
FB_TYPE_FOURCC = 5

FB_VISUAL_MONO01 = 0
FB_VISUAL_MONO10 = 1
FB_VISUAL_TRUECOLOR = 2
FB_VISUAL_PSEUDOCOLOR = 3
FB_VISUAL_DIRECTCOLOR = 4
FB_VISUAL_STATIC_PSEUDOCOLOR = 5
FB_VISUAL_FOURCC = 6

FB_BLANK_UNBLANK = 0
FB_BLANK_POWERDOWN = 4


class Bitfield:  # pylint: disable=too-few-public-methods
    def __init__(self, offset, length, msb_right):
        self.offset = offset
        self.length = length
        self.msb_right = msb_right


# Kind of like a pygame Surface object, or not!
# http://www.pygame.org/docs/ref/surface.html
class Framebuffer:  # pylint: disable=too-many-instance-attributes
    def __init__(self, dev):
        self.dev = dev
        self.fbfd = os.open(dev, os.O_RDWR)
        vinfo = struct.unpack(
            "8I12I16I4I",
            fcntl.ioctl(self.fbfd, FBIOGET_VSCREENINFO, " " * ((8 + 12 + 16 + 4) * 4)),
        )
        finfo = struct.unpack(
            "16cL4I3HI", fcntl.ioctl(self.fbfd, FBIOGET_FSCREENINFO, " " * 48)
        )

        bytes_per_pixel = (vinfo[6] + 7) // 8
        screensize = vinfo[0] * vinfo[1] * bytes_per_pixel

        fbp = mmap.mmap(
            self.fbfd, screensize, flags=mmap.MAP_SHARED, prot=mmap.PROT_READ
        )

        self.fbp = fbp
        self.xres = vinfo[0]
        self.yres = vinfo[1]
        self.xoffset = vinfo[4]
        self.yoffset = vinfo[5]
        self.bits_per_pixel = vinfo[6]
        self.bytes_per_pixel = bytes_per_pixel
        self.grayscale = vinfo[7]
        self.red = Bitfield(vinfo[8], vinfo[9], vinfo[10])
        self.green = Bitfield(vinfo[11], vinfo[12], vinfo[13])
        self.blue = Bitfield(vinfo[14], vinfo[15], vinfo[16])
        self.transp = Bitfield(vinfo[17], vinfo[18], vinfo[19])
        self.nonstd = vinfo[20]
        self.name = b"".join([x for x in finfo[0:15] if x != b"\x00"])
        self.type = finfo[18]
        self.visual = finfo[20]
        self.line_length = finfo[24]
        self.screensize = screensize

    def close(self):
        self.fbp.close()
        os.close(self.fbfd)

    def blank(self, blank):
        # Blanking is not supported by all drivers
        try:
            if blank:
                fcntl.ioctl(self.fbfd, FBIOBLANK, FB_BLANK_POWERDOWN)
            else:
                fcntl.ioctl(self.fbfd, FBIOBLANK, FB_BLANK_UNBLANK)
        except IOError:
            pass

    def __str__(self):
        visual_list = [
            "MONO01",
            "MONO10",
            "TRUECOLOR",
            "PSEUDOCOLOR",
            "DIRECTCOLOR",
            "STATIC PSEUDOCOLOR",
            "FOURCC",
        ]
        type_list = [
            "PACKED_PIXELS",
            "PLANES",
            "INTERLEAVED_PLANES",
            "TEXT",
            "VGA_PLANES",
            "FOURCC",
        ]
        visual_name = "unknown"
        if self.visual < len(visual_list):
            visual_name = visual_list[self.visual]
        type_name = "unknown"
        if self.type < len(type_list):
            type_name = type_list[self.type]

        return (
            'mode "%sx%s"\n' % (self.xres, self.yres)
            + "    nonstd %s\n" % self.nonstd
            + "    rgba %s/%s,%s/%s,%s/%s,%s/%s\n"
            % (
                self.red.length,
                self.red.offset,
                self.green.length,
                self.green.offset,
                self.blue.length,
                self.blue.offset,
                self.transp.length,
                self.transp.offset,
            )
            + "endmode\n"
            + "\n"
            + "Frame buffer device information:\n"
            + "    Device      : %s\n" % self.dev
            + "    Name        : %s\n" % self.name
            + "    Size        : (%d, %d)\n" % (self.xres, self.yres)
            + "    Length      : %s\n" % self.screensize
            + "    BPP         : %d\n" % self.bits_per_pixel
            + "    Type        : %s\n" % type_name
            + "    Visual      : %s\n" % visual_name
            + "    LineLength  : %s\n" % self.line_length
        )


device = "/dev/fb0"
fb = Framebuffer(device)
print(fb)

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)

while True:
    t = time.monotonic()
    fb.fbp.seek(0)
    b = fb.fbp.read(fb.screensize)
    fbimage = Image.frombytes("RGBA", (fb.xres, fb.yres), b, "raw")
    b, g, r, a = fbimage.split()
    fbimage = Image.merge("RGB", (r, g, b))
    fbimage = fbimage.resize((width, height))

    disp.image(fbimage, rotation)
    print(1.0 / (time.monotonic() - t))
fb.close()
