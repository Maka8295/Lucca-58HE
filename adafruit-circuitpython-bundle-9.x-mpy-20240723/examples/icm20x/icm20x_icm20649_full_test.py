# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
from adafruit_icm20x import ICM20649, AccelRange, GyroRange


def printNewMax(value, current_max, axis):
    if value > current_max:
        current_max = value
        print(axis, "Max:", current_max)
    return current_max


# pylint:disable=no-member
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

ism = ICM20649(i2c)

ism.accelerometer_range = AccelRange.RANGE_30G
print("Accelerometer range set to: %d g" % AccelRange.string[ism.accelerometer_range])

ism.gyro_range = GyroRange.RANGE_500_DPS
print("Gyro range set to: %d DPS" % GyroRange.string[ism.gyro_range])

ax_max = ay_max = az_max = 0
gx_max = gy_max = gz_max = 0

ism.gyro_data_rate = 125
ism.accelerometer_data_rate = 4095
st = time.monotonic()
while time.monotonic() - st < 0.250:
    print(
        "Accel X:%.2f Y:%.2f Z:%.2f ms^2 Gyro X:%.2f Y:%.2f Z:%.2f degrees/s"
        % (ism.acceleration + ism.gyro)
    )

#     acceleration = ism.acceleration
#     # ax_max = printNewMax(acceleration[0], ax_max, "AX")
#     # ay_max = printNewMax(acceleration[1], ay_max, "AY")
#     # az_max = printNewMax(acceleration[2], az_max, "AZ")

#     gyro = ism.gyro
#     # gx_max = printNewMax(gyro[0], gx_max, "GX")
#     # gy_max = printNewMax(gyro[1], gy_max, "GY")
#     # gz_max = printNewMax(gyro[2], gz_max, "GZ")
