# SPDX-FileCopyrightText: Copyright (c) 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
MacroPad display image demo. Displays a bitmap image on the built-in display.
"""
from adafruit_macropad import MacroPad

macropad = MacroPad()

macropad.display_image("blinka.bmp")

while True:
    pass
