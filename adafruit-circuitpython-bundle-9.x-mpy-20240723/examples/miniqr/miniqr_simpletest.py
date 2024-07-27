# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import sys
import adafruit_miniqr

# For drawing filled rectangles to the console:
out = sys.stdout
WHITE = "\x1b[1;47m  \x1b[40m"
BLACK = "  "


def prettyprint_QR(matrix):
    # white 4-pixel border at top
    for _ in range(4):
        for _ in range(matrix.width + 8):
            out.write(WHITE)
        print()
    for y in range(matrix.height):
        out.write(WHITE * 4)  # 4-pixel border to left
        for x in range(matrix.width):
            if matrix[x, y]:
                out.write(BLACK)
            else:
                out.write(WHITE)
        out.write(WHITE * 4)  # 4-pixel bporder to right
        print()
    # white 4-pixel border at bottom
    for _ in range(4):
        for _ in range(matrix.width + 8):
            out.write(WHITE)
        print()


qr = adafruit_miniqr.QRCode(qr_type=3, error_correct=adafruit_miniqr.L)
qr.add_data(b"https://www.adafruit.com")
qr.make()
print(qr.matrix)
prettyprint_QR(qr.matrix)
