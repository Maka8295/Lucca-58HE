# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_hts221

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
hts = adafruit_hts221.HTS221(i2c)

data_rate = adafruit_hts221.Rate.label[hts.data_rate]
print("Using data rate of: {:.1f} Hz".format(data_rate))
print("")

while True:
    print("Relative Humidity: {:.2f} % rH".format(hts.relative_humidity))
    print("Temperature: {:.2f} C".format(hts.temperature))
    print("")
    time.sleep(1)
