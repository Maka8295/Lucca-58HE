# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import digitalio
import busio
import board
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from adafruit_epd.epd import Adafruit_EPD
from adafruit_epd.ssd1680 import Adafruit_SSD1680

# create the spi device and pins we will need
spi = busio.SPI(board.EPD_SCK, MOSI=board.EPD_MOSI, MISO=None)
epd_cs = digitalio.DigitalInOut(board.EPD_CS)
epd_dc = digitalio.DigitalInOut(board.EPD_DC)
epd_reset = digitalio.DigitalInOut(board.EPD_RESET)
epd_busy = digitalio.DigitalInOut(board.EPD_BUSY)
srcs = None

display = Adafruit_SSD1680(
    122,
    250,
    spi,
    cs_pin=epd_cs,
    dc_pin=epd_dc,
    sramcs_pin=srcs,
    rst_pin=epd_reset,
    busy_pin=epd_busy,
)

display.rotation = 3
# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = display.width
height = display.height
image = Image.new("RGB", (width, height))

WHITE = (0xFF, 0xFF, 0xFF)
BLACK = (0x00, 0x00, 0x00)

# clear the display
display.fill(Adafruit_EPD.WHITE)

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
# empty it
draw.rectangle((0, 0, width, height), fill=WHITE)

# Draw an outline box
draw.rectangle((1, 1, width - 2, height - 2), outline=BLACK, fill=WHITE)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = 5
shape_width = 30
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = padding
# Draw an ellipse.
draw.ellipse((x, top, x + shape_width, bottom), outline=BLACK, fill=WHITE)
x += shape_width + padding
# Draw a rectangle.
draw.rectangle((x, top, x + shape_width, bottom), outline=WHITE, fill=BLACK)
x += shape_width + padding
# Draw a triangle.
draw.polygon(
    [(x, bottom), (x + shape_width / 2, top), (x + shape_width, bottom)],
    outline=BLACK,
    fill=WHITE,
)
x += shape_width + padding
# Draw an X.
draw.line((x, bottom, x + shape_width, top), fill=BLACK)
draw.line((x, top, x + shape_width, bottom), fill=BLACK)
x += shape_width + padding

# Load default font.
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)

# Alternatively load a TTF font.  Make sure the .ttf font
# file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)

# Write two lines of text.
draw.text((x, top), "Hello", font=font, fill=BLACK)
draw.text((x, top + 20), "World!", font=font, fill=BLACK)

display.image(image)
display.display()

time.sleep(10)

blinkaimage = Image.open("examples/epd_bonnet_blinka_250x122.bmp")
display.image(blinkaimage)
display.display()
