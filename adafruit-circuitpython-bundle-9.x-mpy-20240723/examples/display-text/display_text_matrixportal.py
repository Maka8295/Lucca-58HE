# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example shows how to create a display_text label and show it
with a Matrix Portal

Requires:
adafruit_matrixportal - https://github.com/adafruit/Adafruit_CircuitPython_MatrixPortal

Copy it from the current libraries bundle into the lib folder on your device.
"""
import terminalio
from adafruit_matrixportal.matrix import Matrix
from adafruit_display_text import label

matrix = Matrix()
display = matrix.display

text = "Hello\nworld"
text_area = label.Label(terminalio.FONT, text=text)
text_area.x = 1
text_area.y = 4
display.root_group = text_area
while True:
    pass
