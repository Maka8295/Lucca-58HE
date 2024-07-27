# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Custom badge for PyBadge or PyGamer."""
from adafruit_pybadger import pybadger

pybadger.badge_background(
    background_color=pybadger.WHITE,
    rectangle_color=pybadger.PURPLE,
    rectangle_drop=0.2,
    rectangle_height=0.6,
)

pybadger.badge_line(
    text="@circuitpython", color=pybadger.BLINKA_PURPLE, scale=1, padding_above=1
)
pybadger.badge_line(text="Blinka", color=pybadger.WHITE, scale=3, padding_above=2)
pybadger.badge_line(
    text="CircuitPythonista", color=pybadger.WHITE, scale=1, padding_above=1
)
pybadger.badge_line(
    text="she/her", color=pybadger.BLINKA_PINK, scale=2, padding_above=2
)

while True:
    pybadger.show_custom_badge()
