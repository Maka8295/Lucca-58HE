# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_lis331

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
# un-comment the sensor you are using
# lis = H3LIS331(i2c)
lis = adafruit_lis331.LIS331HH(i2c)

# use a nice fast data rate to for maximum resolution
lis.data_rate = adafruit_lis331.Rate.RATE_1000_HZ

# enable the high pass filter without a reference or offset
lis.enable_hpf(
    True, cutoff=adafruit_lis331.RateDivisor.ODR_DIV_100, use_reference=False
)

# you can also uncomment this section to set and use a reference to offset the measurements
# lis.hpf_reference = 50
# lis.enable_hpf(True, cutoff=RateDivisor.ODR_DIV_100, use_reference=True)


# watch in the serial plotter with the sensor still and you will see the
# z-axis value go from the normal around 9.8 with the filter off to near zero with it
# enabled. If you have a reference enabled and set, that will determind the center point.

# If you shake the sensor, you'll still see the acceleration values change! This is the
# Filter removing slow or non-changing values and letting through ones that move more quickly

while True:
    print(lis.acceleration)  # plotter friendly printing
    time.sleep(0.02)
