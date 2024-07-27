# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_adxl34x

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

# For ADXL343
accelerometer = adafruit_adxl34x.ADXL343(i2c)
# For ADXL345
# accelerometer = adafruit_adxl34x.ADXL345(i2c)

accelerometer.enable_freefall_detection()
# alternatively you can specify attributes when you enable freefall detection for more control:
# accelerometer.enable_freefall_detection(threshold=10,time=25)

while True:
    print("%f %f %f" % accelerometer.acceleration)

    print("Dropped: %s" % accelerometer.events["freefall"])
    time.sleep(0.5)
