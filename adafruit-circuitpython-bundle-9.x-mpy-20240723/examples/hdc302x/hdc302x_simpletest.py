# SPDX-FileCopyrightText: 2024 Liz Clark for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""HDC302x simple test"""

import time
import board
import adafruit_hdc302x

i2c = board.I2C()
sensor = adafruit_hdc302x.HDC302x(i2c)

while True:
    print(f"Temperature: {sensor.temperature:0.1f}°C")
    print(f"Relative Humidity: {sensor.relative_humidity:0.1f}%")
    print()
    time.sleep(2)
