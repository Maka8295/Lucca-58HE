# SPDX-FileCopyrightText: 2023 Jose D. Montoya
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_mlx90393

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
SENSOR = adafruit_mlx90393.MLX90393(i2c, gain=adafruit_mlx90393.GAIN_1X)


while True:
    temp = SENSOR.temperature

    print("Temperature: {} °C".format(temp))

    # Display the status field if an error occurred, etc.
    if SENSOR.last_status > adafruit_mlx90393.STATUS_OK:
        SENSOR.display_status()
    time.sleep(1.0)
