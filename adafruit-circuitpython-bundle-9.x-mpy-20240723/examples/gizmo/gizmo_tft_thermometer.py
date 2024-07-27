# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example will initialize the display using displayio and draw a bmp image
background, and overlay text containing the value read from the on-board temperature sensor.
User may press the A button to switch between celsius and fahrenheit units.

Required libraries:
* Adafruit_CircuitPython_Gizmo
* Adafruit_CircuitPython_ST7789
* Adafruit_CircuitPython_Display_Text
* Adafruit_CircuitPython_CircuitPlayground
"""
import time
from adafruit_circuitplayground import cp
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_gizmo import tft_gizmo

display = tft_gizmo.TFT_Gizmo()


# text scaling factor
TEXT_SCALE = 2

# previous iteration button value
old_a_val = cp.button_a

# boolean for current unit type
show_c_units = True


# function to convert celsius degrees to fahrenheit
def c_to_f(c_val):
    return (c_val * 9 / 5) + 32


# Open the background image file
with open("/thermometer_background.bmp", "rb") as bitmap_file:
    # Setup the file as the bitmap data source
    bitmap = displayio.OnDiskBitmap(bitmap_file)

    # Create a TileGrid to hold the bitmap
    # CircuitPython 6 & 7 compatible
    tile_grid = displayio.TileGrid(
        bitmap,
        pixel_shader=getattr(bitmap, "pixel_shader", displayio.ColorConverter()),
    )
    # CircuitPython 7 compatible only
    # tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)

    # Create a Group to hold the TileGrid
    group = displayio.Group()

    # Add the TileGrid to the Group
    group.append(tile_grid)

    # variable with initial text value, temperature rounded to 2 places
    text = "%.2f C" % (round(cp.temperature, 2))

    # Create a Group for the text so we can scale it
    text_group = displayio.Group(scale=TEXT_SCALE, x=0, y=0)

    # Create a Label to show the initial temperature value
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)

    # Set the anchor_point for center,top
    text_area.anchor_point = (0.5, 0.0)

    # Set the location to center of display, accounting for text_scale
    text_area.anchored_position = (240 / (2 * TEXT_SCALE), 240 / (2 * TEXT_SCALE))

    # Subgroup for text scaling
    text_group.append(text_area)

    # Add the text_group to main Group
    group.append(text_group)

    # Add the main Group to the Display
    display.root_group = group

    # Loop forever
    while True:
        # set current button state to variable
        cur_a_val = cp.button_a
        if cur_a_val and not old_a_val:  # if the button was released
            print("Just released")
            # flip the units boolean to the opposite value
            show_c_units = not show_c_units

        if show_c_units:
            # Update the text
            text_area.text = "%.2f C" % (round(cp.temperature, 2))
        else:  # show f units
            # Update the text
            text_area.text = "%.2f F" % (round(c_to_f(cp.temperature), 2))

        # set previous button value for next time
        old_a_val = cur_a_val
        # Wait a little bit
        time.sleep(0.2)
