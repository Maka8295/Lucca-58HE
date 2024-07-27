# SPDX-FileCopyrightText: 2022 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_adxl37x

i2c = board.STEMMA_I2C()  # uses board.SCL and board.SDA
accelerometer = adafruit_adxl37x.ADXL375(i2c)

accelerometer.offset = 0, 0, 0

print("Hold accelerometer flat to set offsets to 0, 0, and -1g...")
time.sleep(1)
x = accelerometer.raw_x
y = accelerometer.raw_y
z = accelerometer.raw_z
print("Raw x: ", x)
print("Raw y: ", y)
print("Raw z: ", z)

accelerometer.offset = (
    round(-x / 4),
    round(-y / 4),
    round(-(z - 20) / 4),  # Z should be '20' at 1g (49mg per bit)
)
print("Calibrated offsets: ", accelerometer.offset)

while True:
    print("%f %f %f m/s^2" % accelerometer.acceleration)
    time.sleep(0.2)
