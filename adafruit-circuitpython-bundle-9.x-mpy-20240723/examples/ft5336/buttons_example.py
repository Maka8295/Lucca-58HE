# SPDX-FileCopyrightText: 2024 Liz Clark for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Touch buttons example for HX83570 + FT5336 TFT Breakout
"""

import time
import board
import displayio
import terminalio
from adafruit_hx8357 import HX8357
from adafruit_button import Button
import adafruit_ft5336

displayio.release_displays()

spi = board.SPI()
# for eyespi bff
# tft_cs = board.TX
# tft_dc = board.RX
# else:
tft_cs = board.D9
tft_dc = board.D10

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
# display is rotated to align x, y with touch screen x, y
display = HX8357(display_bus, width=320, height=480, rotation=270)

i2c = board.I2C()  # uses board.SCL and board.SDA
touch = adafruit_ft5336.Adafruit_FT5336(i2c)

splash = displayio.Group()
display.root_group = splash

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

spots = [
    {"label": "1", "pos": (10, 10), "color": RED},
    {"label": "2", "pos": (165, 10), "color": YELLOW},
    {"label": "3", "pos": (10, 245), "color": GREEN},
    {"label": "4", "pos": (165, 245), "color": BLUE},
]

buttons = []
for spot in spots:
    button = Button(
        x=spot["pos"][0],
        y=spot["pos"][1],
        width=145,
        height=225,
        style=Button.ROUNDRECT,
        fill_color=spot["color"],
        outline_color=0xFFFFFF,
        label=spot["label"],
        label_font=terminalio.FONT,
        label_color=0x000000,
    )
    splash.append(button)
    buttons.append(button)

display.root_group = splash

button_states = [False for _ in buttons]

while True:
    if touch.touched:
        t = touch.points
        print(t)
        # reset state
        button_states = [False for _ in buttons]
        for point in t:
            for button_index, button in enumerate(buttons):
                if button.contains(point[0:2]):
                    # if button contains point, set state to True
                    button_states[button_index] = True
                    break
        # selected state == button state
        for button_index, button in enumerate(buttons):
            button.selected = button_states[button_index]
    else:
        # if no touch points, then no buttons are selected
        for button in buttons:
            button.selected = False

    time.sleep(0.1)
