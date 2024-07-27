# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# class of sparklines in CircuitPython
# created by Kevin Matocha - Copyright 2020 (C)

# See the bottom for a code example using the `sparkline` Class.

# # File: display_shapes_sparkline.py
# A sparkline is a scrolling line graph, where any values added to sparkline
# using `add_value` are plotted.
#
# The `sparkline` class creates an element suitable for adding to the display
# using `display.root_group = mySparkline` or adding to a `displayio.Group` to be displayed.
#
# When creating the sparkline, identify the number of `max_items` that will be
# included in the graph.
# When additional elements are added to the sparkline and the number of items
# has exceeded max_items, any excess values are removed from the left of the
# graph, and new values are added to the right.


# The following is an example that shows the

# setup display
# instance sparklines
# add to the display
# Loop the following steps:
# 	add new values to sparkline `add_value`
# 	update the sparklines `update`

import random
import time
import board
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_display_shapes.sparkline import Sparkline


if "DISPLAY" not in dir(board):
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

    print("spi.frequency: {}".format(spi.frequency))

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
else:
    # built-in display
    display = board.DISPLAY
    DISPLAY_WIDTH = board.DISPLAY.width

##########################################
# Create background bitmaps and sparklines
##########################################

# Baseline size of the sparkline chart, in pixels.
chart_width = 50
chart_height = 50

font = terminalio.FONT

# Setup the first bitmap and sparkline
# This sparkline has no background bitmap
# sparkline1 uses a vertical y range between -1 to +1.25 and will contain a maximum of 40 items
sparkline1 = Sparkline(
    width=chart_width,
    height=chart_height,
    max_items=40,
    y_min=-1,
    y_max=1.25,
    x=10,
    y=10,
)

# Label the y-axis range
text_label1a = label.Label(
    font=font, text=str(sparkline1.y_top), color=0xFFFFFF
)  # y_top label
text_label1a.anchor_point = (0, 0.5)  # set the anchorpoint
text_label1a.anchored_position = (
    10 + chart_width,
    10,
)  # set the text anchored position to the upper right of the graph

text_label1b = label.Label(
    font=font, text=str(sparkline1.y_bottom), color=0xFFFFFF
)  # y_bottom label
text_label1b.anchor_point = (0, 0.5)  # set the anchorpoint
text_label1b.anchored_position = (
    10 + chart_width,
    10 + chart_height,
)  # set the text anchored position to the upper right of the graph


# Setup the second bitmap and sparkline
# sparkline2 uses a vertical y range between 0 to 1, and will contain a
# maximum of 10 items
#
palette2 = displayio.Palette(1)  # color palette used for bitmap2 (one color)
palette2[0] = 0x0000FF

bitmap2 = displayio.Bitmap(chart_width * 2, chart_height * 2, 1)  # create bitmap2
tilegrid2 = displayio.TileGrid(
    bitmap2, pixel_shader=palette2, x=150, y=10
)  # Add bitmap2 to tilegrid2
sparkline2 = Sparkline(
    width=chart_width * 2,
    height=chart_height * 2,
    max_items=10,
    y_min=0,
    y_max=1,
    x=150,
    y=10,
    color=0xFF00FF,
)


# Setup the third bitmap and third sparkline
# sparkline3 contains a maximum of 10 items
# since y_min and y_max are not specified, sparkline3 uses autoranging for both
# the top and bottom of the y-axis.
# Note1: Any unspecified edge limit (y_min or y_max) will autorange that edge based
# on the data in the list.
# Note2: You can read back the current value of the y-axis limits by using
# sparkline3.y_bottom or sparkline3.y_top


palette3 = displayio.Palette(1)  # color palette used for bitmap (one color)
palette3[0] = 0x11FF44
bitmap3 = displayio.Bitmap(DISPLAY_WIDTH - 30, chart_height * 2, 1)  # create bitmap3
tilegrid3 = displayio.TileGrid(
    bitmap3, pixel_shader=palette3, x=0, y=120
)  # Add bitmap3 to tilegrid3

sparkline3 = Sparkline(
    width=DISPLAY_WIDTH - 30,
    height=chart_height * 2,
    max_items=10,
    x=0,
    y=120,
    color=0xFFFFFF,
)

# Initialize the y-axis labels for mySparkline3 with no text
text_label3a = label.Label(font=font, text="", color=0x11FF44)  # y_top label
text_label3a.anchor_point = (0, 0.5)  # set the anchorpoint
text_label3a.anchored_position = (
    sparkline3.width,
    120,
)  # set the text anchored position to the upper right of the graph

text_label3b = label.Label(font=font, text="", color=0x11FF44)  # y_bottom label
text_label3b.anchor_point = (0, 0.5)  # set the anchorpoint
text_label3b.anchored_position = (
    sparkline3.width,
    120 + sparkline3.height,
)  # set the text anchored position to the upper right of the graph

# Create a group to hold the three bitmap TileGrids and the three sparklines and
# append them into the group (my_group)
#
# Note: In cases where display elements will overlap, then the order the elements
# are added to the group will set which is on top.  Latter elements are displayed
# on top of former elements.
my_group = displayio.Group()

my_group.append(sparkline1)
my_group.append(text_label1a)
my_group.append(text_label1b)

my_group.append(tilegrid2)
my_group.append(sparkline2)

my_group.append(tilegrid3)
my_group.append(sparkline3)
my_group.append(text_label3a)
my_group.append(text_label3b)

# Set the display to show my_group that contains all the bitmap TileGrids and
# sparklines
display.root_group = my_group

i = 0  # This is a counter for changing the random values for mySparkline3

# Start the main loop
while True:
    # Turn off auto_refresh to prevent partial updates of the screen during updates
    # of the sparklines
    display.auto_refresh = False

    # add_value: add a new value to a sparkline
    # Note: The y-range for sparkline1 is set to -1 to 1.25, so all these random
    # values (between 0 and 1) will fit within the visible range of this sparkline
    sparkline1.add_value(random.uniform(0, 1))

    # Note: For sparkline2, the y-axis range is set from 0 to 1.
    # With the random values set between -1 and +2, the values will sometimes
    # be out of the y-range.  This example shows how the fixed y-range (0 to 1)
    # will "clip" values (it will not display them) that are above or below the
    # y-range.
    sparkline2.add_value(random.uniform(-1, 2))

    # sparkline3 is set autoranging for both the top and bottom of the Y-axis

    # In this example, for 15 values, this adds points in the range from 0 to 1.
    # Then, for the next 15 values, it adds points in the range of 0 to 10.
    # This is to highlight the autoranging of the y-axis.
    # Notice how the y-axis labels show that the y-scale is changing.
    #
    # An exercise for the reader: You can set only one or the other sparkline axis
    # to autoranging by setting its value to None.
    if i < 15:
        sparkline3.add_value(random.uniform(0, 1))
    else:
        sparkline3.add_value(random.uniform(0, 10))
    text_label3a.text = str(sparkline3.y_top)
    text_label3b.text = str(sparkline3.y_bottom)
    i += 1  # increment the counter
    if i > 30:  # After 30 times through the loop, reset the counter
        i = 0

    # Turn on auto_refresh for the display
    display.auto_refresh = True

    # The display seems to be less jittery if a small sleep time is provided
    # You can adjust this to see if it has any effect
    time.sleep(0.01)
