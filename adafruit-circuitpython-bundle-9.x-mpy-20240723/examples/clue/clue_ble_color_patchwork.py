# SPDX-FileCopyrightText: 2019 Kattni Rembor, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
Circuit Python BLE Color Patchwork
This demo uses advertising to broadcast a color of the users choice.
We will show a color "patch" on the screen for every unique device
advertisement that we find.
"""

import time
import random
import board
import displayio
from adafruit_display_text import label
import terminalio
from adafruit_ble import BLERadio
from adafruit_ble.advertising.adafruit import AdafruitColor
from adafruit_display_shapes.rect import Rect
from adafruit_clue import clue

MODE_COLOR_SELECT = 0
MODE_SHOW_PATCHWORK = 1

COLOR_TRANSPARENT_INDEX = 0
COLOR_OFFWHITE_INDEX = 1

PROXIMITY_LIMIT = 100

current_mode = MODE_SHOW_PATCHWORK

# The color pickers will cycle through this list with buttons A and B.
color_options = [
    0xEE0000,
    0xEEEE00,
    0x00EE00,
    0x00EEEE,
    0x0000EE,
    0xEE00EE,
    0xCCCCCC,
    0xFF9999,
    0x99FF99,
    0x9999FF,
]


# make all pixels in the patchwork bitmap transparent
def make_transparent():
    palette_mapping.make_transparent(0)
    for i in range(0, 8):
        for j in range(0, 8):
            bitmap[i, j] = 0


# make the pixels in the patchwork white by setting them in the palette
def make_white():
    for i in range(2, 66):
        palette_mapping[i] = 0xFFFFFF


# draw the patchwork grid based on nearby_colors
def draw_grid():
    for i, color in enumerate(nearby_colors):
        if i < 64:
            palette_mapping[i + 2] = (
                color & 0xFFFFFF
            )  # Mask 0xFFFFFF to avoid invalid color.
            print(i)
            print(color)


# create a fake mac address and color for testing
def add_fake():
    fake_mac = "".join([random.choice("0123456789abcdef") for _ in range(10)])
    fake_color = random.choice(color_options)
    nearby_addresses.append(fake_mac)
    nearby_colors.append(fake_color)


# find nearby devices advertising colors
def ble_scan():
    print("scanning")
    # loop over all found devices
    for entry in ble.start_scan(AdafruitColor, minimum_rssi=-100, timeout=1):
        # if this device is not in the list already
        if entry.color in color_options:
            print("new color")
        if entry.address.address_bytes not in nearby_addresses:
            # print(entry.color)
            # add the address and color to respective lists
            nearby_addresses.append(entry.address.address_bytes)
            nearby_colors.append(entry.color)
        else:  # address was already in the list
            # update the color to currently advertised value
            _index = nearby_addresses.index(entry.address.address_bytes)
            nearby_colors[_index] = entry.color


# set a new color to be advertised
def change_advertisement(color):
    ble.stop_advertising()
    advertisement.color = color
    ble.start_advertising(advertisement)
    # set NeoPixel to selected advertised
    clue.pixel.fill(color)
    # update top left self patch
    nearby_colors[0] = color


# BLE Setup
ble = BLERadio()
advertisement = AdafruitColor()
advertisement.color = color_options[0]

# init neopixel
clue.pixel.fill(color_options[0])
clue.pixel.brightness = 0.05

display = board.DISPLAY

# Create a bitmap with two colors + 64 colors for the map
bitmap = displayio.Bitmap(8, 8, 64 + 2)

# Create a 8*8 bitmap pre-filled with 64 colors (color 0 and 1 are reserved)
for _i in range(0, 8):
    for _j in range(0, 8):
        bitmap[_i, _j] = 2 + _i + _j * 8

# Create an empty palette that will be used in one to one mapping
palette_mapping = displayio.Palette(64 + 2)

palette_mapping[0] = 0x000000
palette_mapping[1] = 0xFFFFFF

color_select_palette = displayio.Palette(len(color_options))
for _i, _color in enumerate(color_options):
    color_select_palette[_i] = _color

# Color Select Layout
color_select_group = displayio.Group()
color_select_text_group = displayio.Group(scale=3)

# white background
background = Rect(0, 0, 240, 240, fill=0xFFFFFF)
center_line = Rect(119, 0, 2, 180, fill=0x000000)

# box around the color preview
bottom_box = Rect(79, 174, 80, 80, fill=0xFFFFFF, outline=0x000000, stroke=2)

left_btn_lbl = label.Label(terminalio.FONT, text="A", color=0x000000)
right_btn_lbl = label.Label(terminalio.FONT, text="B", color=0x000000)

left_btn_action = label.Label(
    terminalio.FONT, text="Next\nColor", color=0x000000, line_spacing=1
)
right_btn_action = label.Label(terminalio.FONT, text="Save", color=0x000000)

color_select_text_group.append(left_btn_lbl)
color_select_text_group.append(right_btn_lbl)

color_select_text_group.append(left_btn_action)
color_select_text_group.append(right_btn_action)

# x position centered on 25% of screen
left_btn_lbl.anchor_point = (0.5, 0)
left_btn_lbl.anchored_position = ((240 / 4) // 3, 21 // 3)

# x position centered on 75% of screen
right_btn_lbl.anchor_point = (0.5, 0)
right_btn_lbl.anchored_position = ((240 / 4), 21 // 3)

# x position centered on 25% of screen
left_btn_action.anchor_point = (0.5, 0)
left_btn_action.anchored_position = ((240 / 4) // 3, 96 // 3)

# x position centered on 75% of screen
right_btn_action.anchor_point = (0.5, 0)
right_btn_action.anchored_position = ((240 / 4), 96 // 3)

color_select_group.append(background)
color_select_group.append(center_line)
color_select_group.append(bottom_box)
color_select_group.append(color_select_text_group)

# color preview bmp
color_select_preview_bmp = displayio.Bitmap(1, 1, len(color_options))
color_preview_group = displayio.Group(scale=30 * 2)

# centered horizontally near bottom on screen
color_preview_group.x = 240 // 2 - 60 // 2
color_preview_group.y = 240 - (60 + 2)

color_preview_tilegrid = displayio.TileGrid(
    color_select_preview_bmp, pixel_shader=color_select_palette
)
color_preview_group.append(color_preview_tilegrid)

# Create a TileGrid using the Bitmap and Palette
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette_mapping)
patchwork_group = displayio.Group(scale=30)
patchwork_group.append(tile_grid)

# Create main Group
group = displayio.Group()

# Add the patchwork to the main
group.append(patchwork_group)

# Add the Group to the Display
display.root_group = group

cur_color = 0

prev_b = clue.button_b
prev_a = clue.button_a

nearby_addresses = ["myself"]
nearby_colors = [color_options[cur_color]]

make_white()

last_scan_time = -30
SCAN_INTERVAL = 30  # seconds

while True:
    now = time.monotonic()
    cur_a = clue.button_a
    cur_b = clue.button_b
    if current_mode == MODE_SHOW_PATCHWORK:
        # a button was pressed
        if cur_a and not prev_a:
            current_mode = MODE_COLOR_SELECT

            # insert color select layout
            group.append(color_select_group)
            group.append(color_preview_group)

        # is it time to scan?
        if last_scan_time + SCAN_INTERVAL < now:
            ble_scan()
            last_scan_time = now
            print("after scan found {} results".format(len(nearby_colors)))
            # print(nearby_addresses)
            draw_grid()

        if clue.proximity >= PROXIMITY_LIMIT:
            clue.white_leds = True
            while clue.proximity >= PROXIMITY_LIMIT:
                r, g, b, w = clue.color
                clue.pixel.fill(((r >> 8) & 0xFF, (g >> 8) & 0xFF, (b >> 8) & 0xFF))
                change_advertisement(
                    ((r & 0xFF00) << 8) + (g & 0xFF00) + ((b >> 8) & 0xFF)
                )
                time.sleep(0.1)
            clue.white_leds = False

    elif current_mode == MODE_COLOR_SELECT:
        # current selection preview
        color_select_preview_bmp[0, 0] = cur_color

        # a button was pressed
        if cur_a and not prev_a:
            print("a button")
            # increment currently selected color index
            cur_color += 1
            # reset to 0 if it's too big
            if cur_color >= len(color_options):
                cur_color = 0
            print(cur_color)
        # b button was pressed
        if cur_b and not prev_b:
            print("b button")
            # advertise new color selection
            change_advertisement(color_options[cur_color])

            # go back to patchwork mode
            current_mode = MODE_SHOW_PATCHWORK
            # remove color select background
            group.remove(color_select_group)
            group.remove(color_preview_group)
            make_white()
            draw_grid()
    prev_a = cur_a
    prev_b = cur_b
