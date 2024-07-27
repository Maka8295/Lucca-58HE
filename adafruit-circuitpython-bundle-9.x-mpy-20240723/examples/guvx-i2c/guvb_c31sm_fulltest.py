# SPDX-FileCopyrightText: Copyright (c) 2022 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time
import board
import adafruit_guvx_i2c

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = adafruit_guvx_i2c.GUVB_C31SM(i2c)

# You can select four different power modes: GUVXI2C_PMODE_NORMAL,
# GUVXI2C_PMODE_LOWPOWER, GUVXI2C_PMODE_AUTOSHUT, or UVXI2C_PMODE_SHUTDOWN
# NORMAL is recommended to start!
sensor.power_mode = adafruit_guvx_i2c.GUVXI2C_PMODE_NORMAL
powermodes = ("Normal", "Low power", "Auto shutdown", "Shutdown")
print("Power mode is:", powermodes[sensor.power_mode])

# If in low power mode, we can set the sleep duration.
# It can be: 2, 4, 8, 16, 32, 64, 128, or 256 times
# sensor.sleep_duration = 2

# One of four measuring periods in milliseconds: 100, 200, 400 or 800ms
sensor.measure_period = 100
print("Sensor period is", sensor.measure_period, "ms")

# UVB range, can be: 1, 2, 4, 8, 16, 32, 64, or 128 times
sensor.range = 1
print("Sensor range is", sensor.range, "x")

while True:
    print("UVB:", sensor.uvb, "   UV index:", sensor.uv_index)
    time.sleep(1)
