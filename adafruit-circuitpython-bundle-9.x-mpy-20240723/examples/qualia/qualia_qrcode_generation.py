# SPDX-FileCopyrightText: 2021 Jose David M.
# SPDX-FileCopyrightText: 2023 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# NOTE: Make sure you've set up your settings.toml file before running this example
# https://learn.adafruit.com/getting-started-with-web-workflow-using-the-code-editor/
"""
This example shows a web address QR on the display
"""

import time
from adafruit_qualia.graphics import Graphics, Displays
from adafruit_qualia.peripherals import Peripherals

# Background Information
base = Graphics(Displays.ROUND21, default_bg=0x990099)

# Set up Peripherals
peripherals = Peripherals(i2c_bus=base.i2c_bus)

# Set display to show
display = base.display

# WebPage to show in the QR
webpage = "http://www.adafruit.com"

# QR size Information
qr_size = 9  # Pixels
scale = 10

# Create a barcode
base.qrcode(
    webpage,
    qr_size=scale,
    x=(display.width // 2) - ((qr_size + 5) * scale),
    y=(display.height // 2) - ((qr_size + 4) * scale),
)

while True:
    if peripherals.button_up:
        peripherals.backlight = True
    if peripherals.button_down:
        peripherals.backlight = False
    time.sleep(0.1)
