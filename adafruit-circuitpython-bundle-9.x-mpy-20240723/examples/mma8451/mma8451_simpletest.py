# SPDX-FileCopyrightText: 2018 Tony DiCola for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of reading the MMA8451 orientation every second.

import time
import board
import adafruit_mma8451


# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

# Initialize MMA8451 module.
sensor = adafruit_mma8451.MMA8451(i2c)
# Optionally change the address if it's not the default:
# sensor = adafruit_mma8451.MMA8451(i2c, address=0x1C)

# Optionally change the range from its default of +/-4G:
# sensor.range = adafruit_mma8451.RANGE_2G  # +/- 2G
# sensor.range = adafruit_mma8451.RANGE_4G  # +/- 4G (default)
# sensor.range = adafruit_mma8451.RANGE_8G  # +/- 8G

# Optionally change the data rate from its default of 800hz:
# sensor.data_rate = adafruit_mma8451.DATARATE_800HZ  #  800Hz (default)
# sensor.data_rate = adafruit_mma8451.DATARATE_400HZ  #  400Hz
# sensor.data_rate = adafruit_mma8451.DATARATE_200HZ  #  200Hz
# sensor.data_rate = adafruit_mma8451.DATARATE_100HZ  #  100Hz
# sensor.data_rate = adafruit_mma8451.DATARATE_50HZ   #   50Hz
# sensor.data_rate = adafruit_mma8451.DATARATE_12_5HZ # 12.5Hz
# sensor.data_rate = adafruit_mma8451.DATARATE_6_25HZ # 6.25Hz
# sensor.data_rate = adafruit_mma8451.DATARATE_1_56HZ # 1.56Hz

# Main loop to print the acceleration and orientation every second.
while True:
    x, y, z = sensor.acceleration
    print(
        "Acceleration: x={0:0.3f}m/s^2 y={1:0.3f}m/s^2 z={2:0.3f}m/s^2".format(x, y, z)
    )
    orientation = sensor.orientation
    # Orientation is one of these values:
    #  - PL_PUF: Portrait, up, front
    #  - PL_PUB: Portrait, up, back
    #  - PL_PDF: Portrait, down, front
    #  - PL_PDB: Portrait, down, back
    #  - PL_LRF: Landscape, right, front
    #  - PL_LRB: Landscape, right, back
    #  - PL_LLF: Landscape, left, front
    #  - PL_LLB: Landscape, left, back
    print("Orientation: ", end="")
    if orientation == adafruit_mma8451.PL_PUF:
        print("Portrait, up, front")
    elif orientation == adafruit_mma8451.PL_PUB:
        print("Portrait, up, back")
    elif orientation == adafruit_mma8451.PL_PDF:
        print("Portrait, down, front")
    elif orientation == adafruit_mma8451.PL_PDB:
        print("Portrait, down, back")
    elif orientation == adafruit_mma8451.PL_LRF:
        print("Landscape, right, front")
    elif orientation == adafruit_mma8451.PL_LRB:
        print("Landscape, right, back")
    elif orientation == adafruit_mma8451.PL_LLF:
        print("Landscape, left, front")
    elif orientation == adafruit_mma8451.PL_LLB:
        print("Landscape, left, back")
    time.sleep(1.0)
