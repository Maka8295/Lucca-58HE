# SPDX-FileCopyrightText: 2023 Melissa LeBlanc-Williams for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
Simple painting demo that works with on any touch display
"""
import displayio
from adafruit_qualia.graphics import Graphics, Displays

# For other displays:
# 2.1" Round = Displays.ROUND21
# 3.4" Square = Displays.SQUARE34
# 320 x 820 Bar - Displays.BAR320X820
graphics = Graphics(Displays.SQUARE40, default_bg=None, auto_refresh=False)

if graphics.touch is None:
    raise RuntimeError("This example requires a touch screen.")

# Main Program
pixel_size = 6
palette_width = 160
palette_height = graphics.display.height // 8

bitmap = displayio.Bitmap(graphics.display.width, graphics.display.height, 65535)

# Create a TileGrid to hold the bitmap
tile_grid = displayio.TileGrid(
    bitmap,
    pixel_shader=displayio.ColorConverter(input_colorspace=displayio.Colorspace.RGB565),
)

# Add the TileGrid to the Group
graphics.splash.append(tile_grid)

# Add the Group to the Display
graphics.display.root_group = graphics.splash

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

graphics.display.auto_refresh = True

while True:
    if graphics.touch.touched:
        try:
            for touch in graphics.touch.touches:
                x = touch["x"]
                y = touch["y"]
                if (
                    not 0 <= x < graphics.display.width
                    or not 0 <= y < graphics.display.height
                ):
                    continue  # Skip out of bounds touches
                if x < palette_width:
                    current_color = bitmap[x, y]
                else:
                    for i in range(pixel_size):
                        for j in range(pixel_size):
                            x_pixel = x - (pixel_size // 2) + i
                            y_pixel = y - (pixel_size // 2) + j

                            if (
                                0 <= x_pixel < graphics.display.width
                                and 0 <= y_pixel < graphics.display.height
                            ):
                                bitmap[x_pixel, y_pixel] = current_color
        except RuntimeError:
            pass
