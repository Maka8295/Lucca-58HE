# SPDX-FileCopyrightText: Copyright (c) 2022 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time
import board
from adafruit_debug_i2c import DebugI2C
import adafruit_guvx_i2c


i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

debug_i2c = DebugI2C(i2c)

sensor = adafruit_guvx_i2c.GUVA_C32SM(i2c)

sensor.power_mode = adafruit_guvx_i2c.GUVXI2C_PMODE_NORMAL
powermodes = ("Normal", "Low power", "Auto shutdown", "Shutdown")
print("Power mode is:", powermodes[sensor.power_mode])

# One of four measuring periods in milliseconds: 100, 200, 400 or 800ms
sensor.measure_period = 100
print("Sensor period is", sensor.measure_period, "ms")

# UVA range, can be: 1, 2, 4, 8, 16, 32, 64, or 128 times
sensor.range = 1
print("Sensor range is", sensor.range, "x")

while True:
    print("UVA:", sensor.uva, "   UV index:", sensor.uv_index)
    time.sleep(1)
