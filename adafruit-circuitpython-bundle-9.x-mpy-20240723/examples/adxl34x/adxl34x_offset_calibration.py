# SPDX-FileCopyrightText: 2022 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_adxl34x

i2c = board.STEMMA_I2C()  # uses board.SCL and board.SDA

# For ADXL343
accelerometer = adafruit_adxl34x.ADXL343(i2c)
# For ADXL345
# accelerometer = adafruit_adxl34x.ADXL345(i2c)

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
    round(-x / 8),
    round(-y / 8),
    round(-(z - 250) / 8),  # Z should be '250' at 1g (4mg per bit)
)
print("Calibrated offsets: ", accelerometer.offset)

while True:
    print("%f %f %f m/s^2" % accelerometer.acceleration)
    time.sleep(0.2)
