# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
Simple painting demo that draws on the Adafruit Qualia ESP32-S3 RGB666
with the 4.0" square display and FT6206 captouch driver
"""

import displayio
import busio
import board
import dotclockframebuffer
from framebufferio import FramebufferDisplay
import adafruit_focaltouch

displayio.release_displays()

# Initialize the Display
tft_pins = dict(board.TFT_PINS)

tft_timings = {
    "frequency": 16000000,
    "width": 720,
    "height": 720,
    "hsync_pulse_width": 2,
    "hsync_front_porch": 46,
    "hsync_back_porch": 44,
    "vsync_pulse_width": 2,
    "vsync_front_porch": 16,
    "vsync_back_porch": 18,
    "hsync_idle_low": False,
    "vsync_idle_low": False,
    "de_idle_high": False,
    "pclk_active_high": False,
    "pclk_idle_high": False,
}

init_sequence_tl040hds20 = bytes()

board.I2C().deinit()
i2c = busio.I2C(board.SCL, board.SDA, frequency=100_000)
tft_io_expander = dict(board.TFT_IO_EXPANDER)
# tft_io_expander['i2c_address'] = 0x38 # uncomment for rev B
dotclockframebuffer.ioexpander_send_init_sequence(
    i2c, init_sequence_tl040hds20, **tft_io_expander
)

fb = dotclockframebuffer.DotClockFramebuffer(**tft_pins, **tft_timings)
display = FramebufferDisplay(fb, auto_refresh=False)

# Main Program
pixel_size = 6
palette_width = 160
palette_height = display.height // 8

bitmap = displayio.Bitmap(display.width, display.height, 65535)

# Create a TileGrid to hold the bitmap
tile_grid = displayio.TileGrid(
    bitmap,
    pixel_shader=displayio.ColorConverter(input_colorspace=displayio.Colorspace.RGB565),
)

# Create a Group to hold the TileGrid
group = displayio.Group()

# Add the TileGrid to the Group
group.append(tile_grid)

# Add the Group to the Display
display.root_group = group

display.auto_refresh = True

ft = adafruit_focaltouch.Adafruit_FocalTouch(i2c, address=0x48)

current_color = displayio.ColorConverter().convert(0xFFFFFF)

for i in range(palette_width):
    color_index = i * 255 // palette_width
    rgb565 = displayio.ColorConverter().convert(
        color_index | color_index << 8 | color_index << 16
    )
    r_mask = 0xF800
    g_mask = 0x07E0
    b_mask = 0x001F
    for j in range(palette_height):
        bitmap[i, j + palette_height] = rgb565 & b_mask
        bitmap[i, j + palette_height * 2] = rgb565 & (b_mask | g_mask)
        bitmap[i, j + palette_height * 3] = rgb565 & g_mask
        bitmap[i, j + palette_height * 4] = rgb565 & (r_mask | g_mask)
        bitmap[i, j + palette_height * 5] = rgb565 & r_mask
        bitmap[i, j + palette_height * 6] = rgb565 & (r_mask | b_mask)
        bitmap[i, j + palette_height * 7] = rgb565

while True:
    if ft.touched:
        try:
            for touch in ft.touches:
                x = touch["x"]
                y = touch["y"]
                if x < palette_width:
                    current_color = bitmap[x, y]
                else:
                    for i in range(pixel_size):
                        for j in range(pixel_size):
                            x_pixel = x - (pixel_size // 2) + i
                            y_pixel = y - (pixel_size // 2) + j
                            if (
                                0 <= x_pixel < display.width
                                and 0 <= y_pixel < display.height
                            ):
                                bitmap[x_pixel, y_pixel] = current_color
        except RuntimeError:
            pass
