# SPDX-FileCopyrightText: 2021 Kevin Matocha
#
# SPDX-License-Identifier: MIT
"""
Creates two animated icons with touch response: zoom and shrink animations.
"""
import time
import board
import displayio
import adafruit_touchscreen
from adafruit_displayio_layout.widgets.icon_animated import IconAnimated

display = board.DISPLAY

ts = adafruit_touchscreen.Touchscreen(
    board.TOUCH_XL,
    board.TOUCH_XR,
    board.TOUCH_YD,
    board.TOUCH_YU,
    calibration=((5200, 59000), (5800, 57000)),
    size=(display.width, display.height),
)


IconAnimated.init_class(
    display, max_scale=1.5, max_icon_size=(48, 48), max_color_depth=255
)

icon_zoom = IconAnimated(
    "Zoom",
    "icons/Play_48x48_small.bmp",
    x=50,
    y=40,
    on_disk=True,
    scale=1.5,  # zoom animation
    angle=5,
)

icon_shrink = IconAnimated(
    "Shrink",
    "icons/Play_48x48_small.bmp",
    x=180,
    y=40,
    on_disk=True,
    scale=0.7,  # shrink animation
    angle=-10,
)

icons = [icon_zoom, icon_shrink]

main_group = displayio.Group()
main_group.append(icon_zoom)
main_group.append(icon_shrink)

display.root_group = main_group


COOLDOWN_TIME = 0.25
LAST_PRESS_TIME = -1

display.auto_refresh = True

while True:
    time.sleep(0.05)
    p = ts.touch_point
    if p:
        _now = time.monotonic()
        if _now - LAST_PRESS_TIME > COOLDOWN_TIME:
            for icon in icons:
                if icon.contains(p):
                    icon.zoom_animation(p)
                    LAST_PRESS_TIME = time.monotonic()

    else:
        for icon in icons:
            icon.zoom_out_animation(p)
