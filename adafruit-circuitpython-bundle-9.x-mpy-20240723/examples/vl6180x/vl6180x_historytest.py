# SPDX-FileCopyrightText: 2022 Jonas Schatz
# SPDX-License-Identifier: MIT

# Demo of reading the range from the history buffer of the VL6180x
# distance sensor

import time

import board
import busio

import adafruit_vl6180x


# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Create sensor instance.
sensor = adafruit_vl6180x.VL6180X(i2c)

# Starting continuous mode
print("Starting continuous mode")
sensor.start_range_continuous()

# Main loop prints the ranges every 0.01 seconds for about 5 seconds
# You should see changes 'ripple through' the history array
for _ in range(500):
    # Read the last 16 ranges from the history buffer as a List[int]
    ranges_mm = sensor.ranges_from_history
    print(ranges_mm)

    # Delay for 10 ms so that the loop is not too fast
    time.sleep(0.01)

# Stop continuous mode. This is advised as the sensor
# wouldn't stop measuring after the program has ended
sensor.stop_range_continuous()
