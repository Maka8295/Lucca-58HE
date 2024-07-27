# SPDX-FileCopyrightText: 2018 Jonas Schatz
# SPDX-License-Identifier: MIT

# Demo of reading the range from the VL6180x distance sensor in
# continuous mode

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
sensor.start_range_continuous(20)

# Main loop prints the range and lux every 0.01 seconds
for _ in range(100):
    # Read the range in millimeters and print it.
    range_mm = sensor.range
    print("Range: {0}mm".format(range_mm))

    # Delay for 10 ms
    time.sleep(0.01)

# Stop continuous mode. This is advised as the sensor
# wouldn't stop measuring after the program has ended
sensor.stop_range_continuous()
