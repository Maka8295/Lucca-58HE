# SPDX-FileCopyrightText: 2021 Jose David M.
# SPDX-License-Identifier: MIT

"""
This example shows a web address QR in the display
"""

import board
from adafruit_pyportal.graphics import Graphics

# Set display to show
display = board.DISPLAY

# Background Information
base = Graphics(default_bg=0x990099, debug=True)

# WebPage to show in the QR
webpage = "http://www.adafruit.com"

# QR size Information
qr_size = 9  # Pixels
scale = 3

# Create a barcode
base.qrcode(
    webpage,
    qr_size=scale,
    x=display.width // 2 - qr_size * scale,
    y=display.height // 2 - qr_size * scale,
)

while True:
    pass
