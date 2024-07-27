# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import displayio
import adafruit_miniqr


def bitmap_QR(matrix):
    # monochome (2 color) palette
    BORDER_PIXELS = 2

    # bitmap the size of the screen, monochrome (2 colors)
    bitmap = displayio.Bitmap(
        matrix.width + 2 * BORDER_PIXELS, matrix.height + 2 * BORDER_PIXELS, 2
    )
    # raster the QR code
    for y in range(matrix.height):  # each scanline in the height
        for x in range(matrix.width):
            if matrix[x, y]:
                bitmap[x + BORDER_PIXELS, y + BORDER_PIXELS] = 1
            else:
                bitmap[x + BORDER_PIXELS, y + BORDER_PIXELS] = 0
    return bitmap


qr = adafruit_miniqr.QRCode(qr_type=3, error_correct=adafruit_miniqr.L)
qr.add_data(b"https://www.adafruit.com/circuitpython")
qr.make()

# generate the 1-pixel-per-bit bitmap
qr_bitmap = bitmap_QR(qr.matrix)
# We'll draw with a classic black/white palette
palette = displayio.Palette(2)
palette[0] = 0xFFFFFF
palette[1] = 0x000000
# we'll scale the QR code as big as the display can handle
scale = min(
    board.DISPLAY.width // qr_bitmap.width, board.DISPLAY.height // qr_bitmap.height
)
# then center it!
pos_x = int(((board.DISPLAY.width / scale) - qr_bitmap.width) / 2)
pos_y = int(((board.DISPLAY.height / scale) - qr_bitmap.height) / 2)
qr_img = displayio.TileGrid(qr_bitmap, pixel_shader=palette, x=pos_x, y=pos_y)

splash = displayio.Group(scale=scale)
splash.append(qr_img)
board.DISPLAY.root_group = splash

# Hang out forever
while True:
    pass
