# SPDX-FileCopyrightText: 2024 Tim Cocks for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
from adafruit_display_text.bitmap_label import Label
from terminalio import FONT
from displayio import Group
import adafruit_bme680

# create a main_group to hold anything we want to show on the display.
main_group = Group()

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25

# You will usually have to add an offset to account for the temperature of
# the sensor. This is usually around 5 degrees but varies by use. Use a
# separate temperature sensor to calibrate this one.
temperature_offset = -5

# Create a Label to show the readings. If you have a very small
# display you may need to change to scale=1.
display_output_label = Label(FONT, text="", scale=2)

# place the label near the top left corner with anchored positioning
display_output_label.anchor_point = (0, 0)
display_output_label.anchored_position = (4, 4)

# add the label to the main_group
main_group.append(display_output_label)

# set the main_group as the root_group of the built-in DISPLAY
board.DISPLAY.root_group = main_group

# begin main loop
while True:
    # Update the label.text property to change the text on the display
    display_output_label.text = """Temperature: {:.1f} C
Humidity: {:.1f} %""".format(
        bme680.temperature + temperature_offset, bme680.relative_humidity
    )

    # wait for a bit
    time.sleep(1)
