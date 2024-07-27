# SPDX-FileCopyrightText: 2019 Kattni Rembor, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Calculate the height of an object. Press button A to reset initial height and then lift the
CLUE to find the height."""
from adafruit_clue import clue

# Set to the sea level pressure in hPa at your location for the most accurate altitude measurement.
clue.sea_level_pressure = 1015

clue_display = clue.simple_text_display(
    text_scale=2,
    colors=(clue.CYAN, 0, clue.RED, clue.RED, 0, clue.YELLOW, 0, clue.GREEN),
)

initial_height = clue.altitude

clue_display[0].text = "Calculate height!"
clue_display[2].text = "Press A to reset"
clue_display[3].text = "initial height!"

while True:
    if clue.button_a:
        initial_height = clue.altitude
        clue.pixel.fill(clue.RED)
    else:
        clue.pixel.fill(0)

    clue_display[5].text = "Altitude: {:.1f} m".format(clue.altitude)
    clue_display[7].text = "Height: {:.1f} m".format(clue.altitude - initial_height)
    clue_display.show()
