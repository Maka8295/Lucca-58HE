# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# VEML6070 Driver Example Code

import time
import board
import adafruit_veml6070

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

uv = adafruit_veml6070.VEML6070(i2c)
# Alternative constructors with parameters
# uv = adafruit_veml6070.VEML6070(i2c, 'VEML6070_1_T')
# uv = adafruit_veml6070.VEML6070(i2c, 'VEML6070_HALF_T', True)

# take 10 readings
for j in range(10):
    uv_raw = uv.uv_raw
    risk_level = uv.get_index(uv_raw)
    print("Reading: {0} | Risk Level: {1}".format(uv_raw, risk_level))
    time.sleep(1)
