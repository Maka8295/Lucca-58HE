# SPDX-FileCopyrightText: 2024 DJDevon3
# SPDX-License-Identifier: MIT
import time
import displayio
import terminalio
import board
import digitalio
from adafruit_hx8357 import HX8357  # TFT Featherwing display driver
import adafruit_stmpe610  # TFT Featherwing V1 touch driver
from adafruit_button.sprite_button import SpriteButton

# 3.5" TFT Featherwing is 480x320
displayio.release_displays()
DISPLAY_WIDTH = 480
DISPLAY_HEIGHT = 320

# Initialize TFT Display
spi = board.SPI()
tft_cs = board.D9
tft_dc = board.D10
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = HX8357(display_bus, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT)
display.rotation = 0
_touch_flip = (False, True)

# Initialize 3.5" TFT Featherwing Touchscreen
ts_cs_pin = digitalio.DigitalInOut(board.D6)
touchscreen = adafruit_stmpe610.Adafruit_STMPE610_SPI(
    board.SPI(),
    ts_cs_pin,
    calibration=((231, 3703), (287, 3787)),
    size=(display.width, display.height),
    disp_rotation=display.rotation,
    touch_flip=_touch_flip,
)

TEXT_WHITE = 0xFFFFFF

# --| Button Config |--
BUTTON_WIDTH = 7 * 16
BUTTON_HEIGHT = 2 * 16
BUTTON_MARGIN = 5

# Defiine the button
button = SpriteButton(
    x=BUTTON_MARGIN,
    y=BUTTON_MARGIN,
    width=BUTTON_WIDTH,
    height=BUTTON_HEIGHT,
    label="MENU",
    label_font=terminalio.FONT,
    label_color=TEXT_WHITE,
    bmp_path="bmps/gradient_button_0.bmp",
    selected_bmp_path="bmps/gradient_button_1.bmp",
    transparent_index=0,
)

main_group = displayio.Group()
main_group.append(button)
display.root_group = main_group

while True:
    p = touchscreen.touch_point
    if p:
        if button.contains(p):
            if not button.selected:
                button.selected = True
                time.sleep(0.25)  # Wait a bit so we can see the button color change
                print("Button Pressed")
        else:
            button.selected = False  # When touch moves outside of button
    else:
        button.selected = False  # When button is released
