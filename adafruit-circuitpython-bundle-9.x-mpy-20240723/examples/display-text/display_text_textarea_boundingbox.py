# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import os
import board
import displayio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label


# the current working directory (where this file is)
cwd = ("/" + __file__).rsplit("/", 1)[0]
fonts = [
    file
    for file in os.listdir(cwd + "/fonts/")
    if (file.endswith(".bdf") and not file.startswith("._"))
]
for i, filename in enumerate(fonts):
    fonts[i] = cwd + "/fonts/" + filename
print(fonts)

##########################################################################
THE_FONT = fonts[0]
DISPLAY_STRING = "A multi-line-\nexample of\n  font bounding!"
WRAP_CHARS = 40

##########################################################################
# Make the display context
splash = displayio.Group()
board.DISPLAY.root_group = splash

# Make a background color fill
color_bitmap = displayio.Bitmap(320, 240, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Load the font
font = bitmap_font.load_font(THE_FONT)
font.load_glyphs(DISPLAY_STRING.encode("utf-8"))

print(DISPLAY_STRING)

text = Label(font, text=DISPLAY_STRING)
text.x = 20
text.y = 100
text.color = 0x0

# Make a background color fill
dims = text.bounding_box
print(dims)
textbg_bitmap = displayio.Bitmap(dims[2], dims[3], 1)
textbg_palette = displayio.Palette(1)
textbg_palette[0] = 0xFF0000
textbg_sprite = displayio.TileGrid(
    textbg_bitmap, pixel_shader=textbg_palette, x=text.x + dims[0], y=text.y + dims[1]
)
splash.append(textbg_sprite)
splash.append(text)
try:
    board.DISPLAY.refresh(target_frames_per_second=60)
except AttributeError:
    board.DISPLAY.refresh_soon()
    board.DISPLAY.wait_for_frame()


while True:
    pass
