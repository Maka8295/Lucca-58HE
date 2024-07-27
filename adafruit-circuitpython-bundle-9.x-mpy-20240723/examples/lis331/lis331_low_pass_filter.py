# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
from adafruit_lis331 import LIS331HH, Rate, Frequency

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

# un-comment the sensor you are using
# lis = H3LIS331(i2c)
lis = LIS331HH(i2c)

# `data_rate` must be a `LOWPOWER` rate to use the low-pass filter
lis.data_rate = Rate.RATE_LOWPOWER_10_HZ
# next set the cutoff frequency. Anything changing faster than
# the specified frequency will be filtered out
lis.lpf_cutoff = Frequency.FREQ_74_HZ

# Once you've seen the filter do its thing, you can comment out the
# lines above to use the default data rate without the low pass filter
# and see the difference it makes

while True:
    print(lis.acceleration)  # plotter friendly printing
    time.sleep(0.002)
