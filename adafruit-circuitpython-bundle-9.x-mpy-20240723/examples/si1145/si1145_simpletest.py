# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Carter Nelson for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time
import board
import adafruit_si1145

# setup I2C bus using board default
# change as needed for specific boards
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

# setup sensor
si1145 = adafruit_si1145.SI1145(i2c)

# loop forever printing values
while True:
    vis, ir = si1145.als
    print("Visible = {}, Infrared = {}".format(vis, ir))
    time.sleep(1)
