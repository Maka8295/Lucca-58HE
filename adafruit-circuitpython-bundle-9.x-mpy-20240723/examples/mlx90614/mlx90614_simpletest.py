# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

#  Designed specifically to work with the MLX90614 sensors in the
#  adafruit shop
#  ----> https://www.adafruit.com/product/1747
#  ----> https://www.adafruit.com/product/1748
#
#  These sensors use I2C to communicate, 2 pins are required to
#  interface Adafruit invests time and resources providing this open
#  source code,
#  please support Adafruit and open-source hardware by purchasing
#  products from Adafruit!

import board
import adafruit_mlx90614

# The MLX90614 only works at the default I2C bus speed of 100kHz.
# A higher speed, such as 400kHz, will not work.
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
mlx = adafruit_mlx90614.MLX90614(i2c)

# temperature results in celsius
print("Ambent Temp: ", mlx.ambient_temperature)
print("Object Temp: ", mlx.object_temperature)
