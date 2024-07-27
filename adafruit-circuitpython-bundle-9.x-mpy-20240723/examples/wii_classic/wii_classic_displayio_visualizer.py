# SPDX-FileCopyrightText: 2023 Liz Clark for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import terminalio
import displayio

# Support 8.x.x and 9.x.x. Can be simplified after 8.x.x is discontinued as a stable release.
try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire

import simpleio
from adafruit_display_text import label
from adafruit_display_shapes.circle import Circle
import adafruit_ili9341
import adafruit_wii_classic

displayio.release_displays()

spi = board.SPI()
tft_cs = board.A2
tft_dc = board.A1

display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=board.A3)
display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240)

bg = displayio.OnDiskBitmap("/wii_classic.bmp")
bg_tilegrid = displayio.TileGrid(bg, pixel_shader=bg.pixel_shader)

# Make the display context
splash = displayio.Group()
splash.append(bg_tilegrid)
display.root_group = splash

i2c = board.STEMMA_I2C()
ctrl_pad = adafruit_wii_classic.Wii_Classic(i2c)

RED = 0xFF0000
BLACK = 0x000000

button_spots = [
    {"label": "dpad_up", "pos": (68, 92), "size": 7, "color": RED},
    {"label": "dpad_down", "pos": (68, 132), "size": 7, "color": RED},
    {"label": "dpad_left", "pos": (48, 112), "size": 7, "color": RED},
    {"label": "dpad_right", "pos": (88, 112), "size": 7, "color": RED},
    {"label": "button_a", "pos": (277, 111), "size": 7, "color": RED},
    {"label": "button_b", "pos": (253, 137), "size": 7, "color": RED},
    {"label": "button_x", "pos": (252, 86), "size": 7, "color": RED},
    {"label": "button_y", "pos": (227, 111), "size": 7, "color": RED},
    {"label": "button_select", "pos": (136, 116), "size": 4, "color": RED},
    {"label": "button_home", "pos": (160, 116), "size": 4, "color": RED},
    {"label": "button_start", "pos": (184, 116), "size": 4, "color": RED},
    {"label": "button_zl", "pos": (134, 42), "size": 12, "color": RED},
    {"label": "button_zr", "pos": (188, 42), "size": 12, "color": RED},
    {"label": "button_lshoulder", "pos": (58, 44), "size": 12, "color": RED},
    {"label": "button_rshoulder", "pos": (259, 44), "size": 12, "color": RED},
]

overlays = []
for spot in button_spots:
    b = Circle(x0=spot["pos"][0], y0=spot["pos"][1], r=spot["size"], fill=spot["color"])
    splash.append(b)
    overlays.append(b)

texts = [
    {"label": "l_x_text", "text": "L_JOY_X: 00", "x": 6, "y": 220, "color": BLACK},
    {"label": "l_y_text", "text": "L_JOY_Y: 00", "x": 88, "y": 220, "color": BLACK},
    {"label": "r_x_text", "text": "R_JOY_X: 00", "x": 173, "y": 220, "color": BLACK},
    {"label": "r_y_text", "text": "R_JOY_X: 00", "x": 248, "y": 220, "color": BLACK},
    {"label": "ls_text", "text": "L_PRESSURE: 00", "x": 10, "y": 11, "color": BLACK},
    {"label": "rs_text", "text": "R_PRESSURE: 00", "x": 220, "y": 11, "color": BLACK},
]

analog_text = []
for text in texts:
    t = label.Label(
        terminalio.FONT,
        text=text["text"],
        color=text["color"],
        x=text["x"],
        y=text["y"],
    )
    splash.append(t)
    analog_text.append(t)

last_l_x = 0
last_r_x = 0
last_l_y = 0
last_r_y = 0
last_r_press = 0
last_l_press = 0

while True:
    l_x, l_y = ctrl_pad.joystick_l
    mapped_l_x = simpleio.map_range(l_x, 7, 58, -50, 50)
    mapped_l_y = simpleio.map_range(l_y, 7, 58, -50, 50)
    r_x, r_y = ctrl_pad.joystick_r
    mapped_r_x = simpleio.map_range(r_x, 2, 26, -50, 50)
    mapped_r_y = simpleio.map_range(r_y, 3, 28, -50, 50)
    left_pressure = ctrl_pad.l_shoulder.LEFT_FORCE
    right_pressure = ctrl_pad.r_shoulder.RIGHT_FORCE
    if last_l_x != mapped_l_x:
        analog_text[0].text = "L_JOY_X: %d" % mapped_l_x
        last_l_x = mapped_l_x
    if last_l_y != mapped_l_y:
        analog_text[1].text = "L_JOY_Y: %d" % mapped_l_y
        last_l_y = mapped_l_y
    if last_r_x != mapped_r_x:
        analog_text[2].text = "R_JOY_X: %d" % mapped_r_x
        last_r_x = mapped_r_x
    if last_r_y != mapped_r_y:
        analog_text[3].text = "R_JOY_Y: %d" % mapped_r_y
        last_r_y = mapped_r_y
    if last_r_press != right_pressure:
        analog_text[4].text = "R_PRESSURE: %d" % right_pressure
        last_r_press = right_pressure
    if last_l_press != left_pressure:
        analog_text[5].text = "L_PRESSURE: %d" % left_pressure
        last_l_press = left_pressure
    if ctrl_pad.d_pad.UP:
        overlays[0].fill = RED
    else:
        overlays[0].fill = BLACK
    if ctrl_pad.d_pad.DOWN:
        overlays[1].fill = RED
    else:
        overlays[1].fill = BLACK
    if ctrl_pad.d_pad.LEFT:
        overlays[2].fill = RED
    else:
        overlays[2].fill = BLACK
    if ctrl_pad.d_pad.RIGHT:
        overlays[3].fill = RED
    else:
        overlays[3].fill = BLACK
    if ctrl_pad.buttons.A:
        overlays[4].fill = RED
    else:
        overlays[4].fill = BLACK
    if ctrl_pad.buttons.B:
        overlays[5].fill = RED
    else:
        overlays[5].fill = BLACK
    if ctrl_pad.buttons.X:
        overlays[6].fill = RED
    else:
        overlays[6].fill = BLACK
    if ctrl_pad.buttons.Y:
        overlays[7].fill = RED
    else:
        overlays[7].fill = BLACK
    if ctrl_pad.buttons.SELECT:
        overlays[8].fill = RED
    else:
        overlays[8].fill = BLACK
    if ctrl_pad.buttons.HOME:
        overlays[9].fill = RED
    else:
        overlays[9].fill = BLACK
    if ctrl_pad.buttons.START:
        overlays[10].fill = RED
    else:
        overlays[10].fill = BLACK
    if ctrl_pad.buttons.ZL:
        overlays[11].fill = RED
    else:
        overlays[11].fill = BLACK
    if ctrl_pad.buttons.ZR:
        overlays[12].fill = RED
    else:
        overlays[12].fill = BLACK
    if ctrl_pad.buttons.L:
        overlays[13].fill = RED
    else:
        overlays[13].fill = BLACK
    if ctrl_pad.buttons.R:
        overlays[14].fill = RED
    else:
        overlays[14].fill = BLACK
