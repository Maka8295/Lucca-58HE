# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Configure the sensor for continuous measurement with rates,
sampling counts and mode optimized for low power, as recommended
in Infineon's datasheet:
https://www.infineon.com/dgdl/Infineon-DPS310-DS-v01_00-EN.pdf
"""

# (disable pylint warnings for adafruit_dps310.{SampleCount,Rate,Mode}.*
# as they are generated dynamically)
# pylint: disable=no-member

import time
import board
from adafruit_dps310 import advanced

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
dps310 = advanced.DPS310_Advanced(i2c)

dps310.reset()
dps310.pressure_oversample_count = advanced.SampleCount.COUNT_2
dps310.pressure_rate = advanced.Rate.RATE_1_HZ
dps310.temperature_oversample_count = advanced.SampleCount.COUNT_16
dps310.temperature_rate = advanced.Rate.RATE_1_HZ
dps310.mode = advanced.Mode.CONT_PRESTEMP
dps310.wait_temperature_ready()
dps310.wait_pressure_ready()

while True:
    print("Temperature = %.2f *C" % dps310.temperature)
    print("Pressure = %.2f hPa" % dps310.pressure)
    print("")
    time.sleep(10.0)
