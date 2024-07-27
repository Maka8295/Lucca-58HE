# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Sample for comparing label and bitmap_label positioning with Builtin or loaded BDF fonts

# pylint: disable=no-member

import gc
import board
import displayio
import terminalio
from adafruit_bitmap_font import bitmap_font

from adafruit_display_text import bitmap_label
from adafruit_display_text import label

# pylint: disable=no-member


##########
# Use this Boolean variables to select which font style to use
##########
use_builtinfont = False  # Set True to use the terminalio.FONT BuiltinFont,
fontToUse = terminalio.FONT
# Set False to use a BDF loaded font, see "fontFiles" below
##########

if not use_builtinfont:
    # load the fonts
    print("loading font...")

    fontList = []

    # Load some proportional fonts
    fontFile = "fonts/LeagueSpartan-Bold-16.bdf"
    fontToUse = bitmap_font.load_font(fontFile)

# Set scaling factor for display text
my_scale = 1

#  Setup the SPI display
if "DISPLAY" in dir(board):
    # use built in display (PyPortal, PyGamer, PyBadge, CLUE, etc.)
    # see guide for setting up external displays (TFT / OLED breakouts, RGB matrices, etc.)
    # https://learn.adafruit.com/circuitpython-display-support-using-displayio/display-and-display-bus
    display = board.DISPLAY

else:
    # Setup the LCD display with driver
    # You may need to change this to match the display driver for the chipset
    # used on your display
    from adafruit_ili9341 import ILI9341

    displayio.release_displays()

    # setup the SPI bus
    spi = board.SPI()
    tft_cs = board.D9  # arbitrary, pin not used
    tft_dc = board.D10
    tft_backlight = board.D12
    tft_reset = board.D11

    while not spi.try_lock():
        spi.configure(baudrate=32000000)
    spi.unlock()

    display_bus = displayio.FourWire(
        spi,
        command=tft_dc,
        chip_select=tft_cs,
        reset=tft_reset,
        baudrate=32000000,
        polarity=1,
        phase=1,
    )

    # Number of pixels in the display
    DISPLAY_WIDTH = 320
    DISPLAY_HEIGHT = 240

    # create the display
    display = ILI9341(
        display_bus,
        width=DISPLAY_WIDTH,
        height=DISPLAY_HEIGHT,
        rotation=180,  # The rotation can be adjusted to match your configuration.
        auto_refresh=True,
        native_frames_per_second=90,
    )

    # reset the display to show nothing.
    display.root_group = None

print("Display is started")

preload_glyphs = (
    True  # set this to True if you want to preload the font glyphs into memory
)
# preloading the glyphs will help speed up the rendering of text but will use more RAM

if preload_glyphs and not use_builtinfont:
    # identify the glyphs to load into memory -> increases rendering speed
    glyphs = (
        b"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/-_,.:?!'\n "
    )

    print("loading glyphs...")
    fontToUse.load_glyphs(glyphs)

    print("Glyphs are loaded.")

print("Fonts completed loading.")

# create group

long_string = "The purple snake\nbrings python fun\nto everyone."
label2_padding = 10

#####
# Create the "bitmap_label.py" versions of the text labels.

gc.collect()
bitmap_label_start = gc.mem_free()

bmap_label1 = bitmap_label.Label(
    font=fontToUse,
    text="bitmap_label",
    color=0xFFFFFF,
    background_color=0xFF0000,
    padding_bottom=0,
    padding_left=0,
    padding_right=0,
    padding_top=0,
    background_tight=True,
    line_spacing=1.25,
    scale=my_scale,
    anchor_point=(0.0, 0),
    anchored_position=(10, 60),
)

bmap_label2 = bitmap_label.Label(
    font=fontToUse,
    text=long_string,
    color=0x000000,
    background_color=0xFFFF00,
    padding_bottom=label2_padding,
    padding_left=0,
    padding_right=0,
    padding_top=label2_padding,
    background_tight=False,
    line_spacing=1.25,
    scale=my_scale,
    anchor_point=(0.0, 0),
    anchored_position=(10, 120),
)

gc.collect()
bitmap_label_end = gc.mem_free()

print("bitmap_label used: {} memory".format(bitmap_label_start - bitmap_label_end))

bmap_group = displayio.Group()  # Create a group for displaying
bmap_group.append(bmap_label1)
bmap_group.append(bmap_label2)


#####
# Create the "label.py" versions of the text labels.

gc.collect()
label_start = gc.mem_free()

label1 = label.Label(
    font=fontToUse,
    text="label",
    color=0xFFFFFF,
    background_color=0xFF0000,
    padding_bottom=0,
    padding_left=0,
    padding_right=0,
    padding_top=0,
    background_tight=True,
    line_spacing=1.25,
    scale=my_scale,
    anchor_point=(1.0, 0),
    anchored_position=(display.width - 10, 60),
)

label2 = label.Label(
    font=fontToUse,
    text=long_string,
    color=0x000000,
    background_color=0xFFFF00,
    padding_bottom=label2_padding,
    padding_left=0,
    padding_right=0,
    padding_top=label2_padding,
    background_tight=False,
    line_spacing=1.25,
    scale=my_scale,
    anchor_point=(1.0, 0),
    anchored_position=(display.width - 10, 120),
)

gc.collect()
label_end = gc.mem_free()

print("label used: {} memory".format(label_start - label_end))
label_group = displayio.Group()  # Create a group for displaying
label_group.append(label1)
label_group.append(label2)


print("***")

main_group = displayio.Group()
main_group.append(label_group)
main_group.append(bmap_group)

display.auto_refresh = True

display.root_group = main_group
while True:
    pass
