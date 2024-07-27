# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of the FXAS21002C gyroscope.
# Will print the gyroscope values every second.
import time
import board
import adafruit_fxas21002c


# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = adafruit_fxas21002c.FXAS21002C(i2c)
# Optionally create the sensor with a different gyroscope range (the
# default is 250 DPS, but you can use 500, 1000, or 2000 DPS values):
# sensor = adafruit_fxas21002c.FXAS21002C(i2c, gyro_range=adafruit_fxas21002c.GYRO_RANGE_500DPS)
# sensor = adafruit_fxas21002c.FXAS21002C(i2c, gyro_range=adafruit_fxas21002c.GYRO_RANGE_1000DPS)
# sensor = adafruit_fxas21002c.FXAS21002C(i2c, gyro_range=adafruit_fxas21002c.GYRO_RANGE_2000DPS)

# Main loop will read the gyroscope values every second and print them out.
while True:
    # Read gyroscope.
    gyro_x, gyro_y, gyro_z = sensor.gyroscope
    # Print values.
    print(
        "Gyroscope (radians/s): ({0:0.3f},  {1:0.3f},  {2:0.3f})".format(
            gyro_x, gyro_y, gyro_z
        )
    )
    # Delay for a second.
    time.sleep(1.0)
