# SPDX-FileCopyrightText: 2024 Liz Clark for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""HDC302x alerts example"""

import time
import board
import adafruit_hdc302x

i2c = board.I2C()
sensor = adafruit_hdc302x.HDC302x(i2c)

high_temp = 28
high_humid = 80
low_temp = 24
low_humid = 54

print("Setting alerts")
sensor.set_high_alert(high_temp, high_humid)
sensor.set_low_alert(low_temp, low_humid)

while True:
    print("Temperature:", sensor.temperature, "C")
    print("Relative Humidity:", sensor.relative_humidity, "%")
    if sensor.high_alert:
        print("High alert triggered!")
        print("Clearing high alert")
        sensor.clear_high_alert(high_temp, high_humid)
    if sensor.low_alert:
        print("Low alert triggered!")
        print("Clearing low alert")
        sensor.clear_low_alert(low_temp, low_humid)
    else:
        print("No alerts triggered")
    print()
    time.sleep(2)
