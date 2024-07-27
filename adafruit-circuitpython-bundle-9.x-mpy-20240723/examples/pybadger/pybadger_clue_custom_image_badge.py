# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Custom image badge example for Adafruit CLUE."""
from adafruit_pybadger import pybadger

pybadger.image_background("Blinka_CLUE.bmp")

pybadger.badge_line(text="@circuitpython", color=pybadger.SKY, scale=2, padding_above=2)
pybadger.badge_line(text="Blinka", color=pybadger.WHITE, scale=5, padding_above=3)
pybadger.badge_line(
    text="CircuitPythonista", color=pybadger.WHITE, scale=2, padding_above=2
)
pybadger.badge_line(text="she/her", color=pybadger.SKY, scale=4, padding_above=4)

while True:
    pybadger.show_custom_badge()
