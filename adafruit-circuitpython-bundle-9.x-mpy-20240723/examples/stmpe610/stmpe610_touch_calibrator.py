# SPDX-FileCopyrightText: 2022 CedarGroveMakerStudios for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
stmpe610_touch_calibrator.py  2022-01-21 v1.1

Author(s): CedarGroveMakerStudios

On-screen touchscreen calibrator for TFT FeatherWing displays.

When the test screen appears, use a stylus to swipe to the four edges
of the visible display area. As the screen is calibrated, the small red
square tracks the stylus tip (REPL_ONLY=False). Minimum and maximum
calibration values will display on the screen and in the REPL. The calibration
tuple can be copied and pasted into the calling code's touchscreen
instantiation statement.

NOTE: When instantiating the STMPE610 controller, enter the 0-degree display
rotation raw touch calibration value regardless of screen rotation value.
The controller code will automatically adjust the calibration as needed.

DISPLAY_ROTATION: Display rotation value in degrees. Only values of
None, 0, 90, 180, and 270 degrees are accepted. Defaults to None, the
previous orientation of the display.

REPL_ONLY: If False, calibration values are shown graphically on the screen
and printed to the REPL. If True, the values are only printed to the REPL.
Default value is False.

RAW_DATA: If True, measure and display the raw touchscreen values. If False,
display the touch value in screen coordinates; requires a previously measured
calibration tuple for screen coordinate conversion accuracy.
"""

import time
import board
import digitalio
import displayio
import vectorio
import terminalio
from adafruit_display_text.label import Label

# from adafruit_hx8357 import HX8357
from adafruit_ili9341 import ILI9341
from simpleio import map_range
import adafruit_stmpe610

# Operational parameters:
#   Specify 0, 90, 180, or 270 degrees;
#   use 0 for instantiation calibration tuple.
DISPLAY_ROTATION = 0
REPL_ONLY = False  # True to disable graphics
RAW_DATA = True  # Use touchscreen raw values; False to use display coordinates

# Previously measured raw calibration tuple for
#   display coordinate mode (RAW_DATA = False):
CALIBRATION = ((357, 3812), (390, 3555))

# A collection of colors used for graphic objects
BLUE_DK = 0x000060  # Screen fill
RED = 0xFF0000  # Boundary
WHITE = 0xFFFFFF  # Text

# Release any resources currently in use for the displays
displayio.release_displays()

# Define the display's SPI bus connection
disp_bus = displayio.FourWire(
    board.SPI(), command=board.D10, chip_select=board.D9, reset=None
)

# Instantiate the 2.4" 320x240 TFT FeatherWing (#3315).
display = ILI9341(disp_bus, width=320, height=240)
_touch_flip = (False, False)

"""# Instantiate the 3.5" 480x320 TFT FeatherWing (#3651).
display = HX8357(disp_bus, width=480, height=320)
_touch_flip = (False, True)"""

# Check rotation value and update display.
# Always set rotation before instantiating the touchscreen.
if DISPLAY_ROTATION is not None and DISPLAY_ROTATION in (0, 90, 180, 270):
    display.rotation = DISPLAY_ROTATION
else:
    print("Warning: invalid rotation value -- defalting to zero")
    display.rotation = 0
    time.sleep(1)

# Activate the display graphics unless REPL_ONLY=True.
if not REPL_ONLY:
    display_group = displayio.Group()
    display.root_group = display_group

# Instantiate touchscreen.
ts_cs = digitalio.DigitalInOut(board.D6)
if RAW_DATA:
    # Display raw touchscreen values; calibration tuple not required.
    ts = adafruit_stmpe610.Adafruit_STMPE610_SPI(
        board.SPI(), ts_cs, disp_rotation=display.rotation, touch_flip=_touch_flip
    )
else:
    # Display calibrated screen coordinates.
    # Update the raw calibration tuple with previously measured values.
    ts = adafruit_stmpe610.Adafruit_STMPE610_SPI(
        board.SPI(),
        ts_cs,
        calibration=CALIBRATION,
        size=(display.width, display.height),
        disp_rotation=display.rotation,
        touch_flip=_touch_flip,
    )

# Define the graphic objects if REPL_ONLY = False.
if not REPL_ONLY:
    # Define the text graphic objects
    font_0 = terminalio.FONT

    coordinates = Label(
        font=font_0,
        text="calib: ((x_min, x_max), (y_min, y_max))",
        color=WHITE,
    )
    coordinates.anchor_point = (0.5, 0.5)
    coordinates.anchored_position = (display.width // 2, display.height // 4)

    display_rotation = Label(
        font=font_0,
        text="rotation: " + str(display.rotation),
        color=WHITE,
    )
    display_rotation.anchor_point = (0.5, 0.5)
    display_rotation.anchored_position = (display.width // 2, display.height // 4 - 30)

    # Define graphic objects for the screen fill, boundary, and touch pen.
    target_palette = displayio.Palette(1)
    target_palette[0] = BLUE_DK
    screen_fill = vectorio.Rectangle(
        pixel_shader=target_palette,
        x=2,
        y=2,
        width=display.width - 4,
        height=display.height - 4,
    )

    target_palette = displayio.Palette(1)
    target_palette[0] = RED
    boundary = vectorio.Rectangle(
        pixel_shader=target_palette,
        x=0,
        y=0,
        width=display.width,
        height=display.height,
    )

    pen = vectorio.Rectangle(
        pixel_shader=target_palette,
        x=display.width // 2,
        y=display.height // 2,
        width=10,
        height=10,
    )

    display_group.append(boundary)
    display_group.append(screen_fill)
    display_group.append(pen)
    display_group.append(coordinates)
    display_group.append(display_rotation)

# Reset x and y values to raw or display size mid-point before measurement.
x = y = 0
if RAW_DATA:
    x_min = y_min = x_max = y_max = 4096 // 2
else:
    x_min = y_min = x_max = y_max = min(display.width, display.height) // 2

print("Touchscreen Calibrator")
print("  Use a stylus to swipe slightly beyond the")
print("  four edges of the visible display area.")
print(" ")
print(f"  display rotation: {display.rotation} degrees")
print("  Calibration values follow:")
print(" ")

while True:
    time.sleep(0.100)
    touch = ts.touch_point  # Check for touch
    if touch:
        x = touch[0]  # Raw touchscreen x value
        y = touch[1]  # Raw touchscreen y value
        if not REPL_ONLY:
            pen.x = int(round(map_range(x, x_min, x_max, 0, display.width), 0)) - 5
            pen.y = int(round(map_range(y, y_min, y_max, 0, display.height), 0)) - 5

        # Remember minimum and maximum values for the calibration tuple.
        x_min = min(x_min, touch[0])
        x_max = max(x_max, touch[0])
        y_min = min(y_min, touch[1])
        y_max = max(y_max, touch[1])

        # Show the calibration tuple.
        print(f"(({x_min}, {x_max}), ({y_min}, {y_max}))")
        if not REPL_ONLY:
            coordinates.text = f"calib: (({x_min}, {x_max}), ({y_min}, {y_max}))"
