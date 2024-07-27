# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
'map_range_demo.py'.

=================================================
maps a number from one range to another
"""
import time
import simpleio

while True:
    sensor_value = 150

    # Map the sensor's range from 0<=sensor_value<=255 to 0<=sensor_value<=1023
    print("original sensor value: ", sensor_value)
    mapped_value = simpleio.map_range(sensor_value, 0, 255, 0, 1023)
    print("mapped sensor value: ", mapped_value)
    time.sleep(2)

    # Map the new sensor value back to the old range
    sensor_value = simpleio.map_range(mapped_value, 0, 1023, 0, 255)
    print("original value returned: ", sensor_value)
    time.sleep(2)
