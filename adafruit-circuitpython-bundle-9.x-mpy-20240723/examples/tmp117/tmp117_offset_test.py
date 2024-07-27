# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import board
import adafruit_tmp117

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

tmp117 = adafruit_tmp117.TMP117(i2c)

print("Temperature without offset: %.2f degrees C" % tmp117.temperature)
tmp117.temperature_offset = 10.0
while True:
    print("Temperature w/ offset: %.2f degrees C" % tmp117.temperature)
    time.sleep(1)
