# SPDX-FileCopyrightText: 2020 by Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
# pylint:disable=no-member
from time import sleep
import board
import busio
from adafruit_mlx90395 import MLX90395, OSR, Resolution, Gain

i2c = busio.I2C(board.SCL, board.SDA)
sensor = MLX90395(i2c)

sensor.oversample_rate = OSR.RATE_1X
# sensor.oversample_rate = OSR.RATE_2X
# sensor.oversample_rate = OSR.RATE_4X
# sensor.oversample_rate = OSR.RATE_8X
print("Oversample Rate:", OSR.string[sensor.oversample_rate])

sensor.resolution = Resolution.BITS_16
# sensor.resolution = Resolution.BITS_17
# sensor.resolution = Resolution.BITS_18
# sensor.resolution = Resolution.BITS_19
print("Resolution:", Resolution.string[sensor.resolution])

sensor.gain = Gain.GAIN_0_2
# sensor.gain = Gain.GAIN_0_25
# sensor.gain = Gain.GAIN_0_3333
# sensor.gain = Gain.GAIN_0_4
# sensor.gain = Gain.GAIN_0_5
# sensor.gain = Gain.GAIN_0_6
# sensor.gain = Gain.GAIN_0_75
# sensor.gain = Gain.GAIN_1
# sensor.gain = Gain.GAIN_0_1
# sensor.gain = Gain.GAIN_0_125
# sensor.gain = Gain.GAIN_0_1667
# sensor.gain = Gain.GAIN_0_2
# sensor.gain = Gain.GAIN_0_25
# sensor.gain = Gain.GAIN_0_3
# sensor.gain = Gain.GAIN_0_375
# sensor.gain = Gain.GAIN_0_5
print("Gain:", Gain.string[sensor.gain])

while True:
    print("X:{0:5.2f}, Y:{1:5.2f}, Z:{2:5.2f} uT".format(*sensor.magnetic))
    print("")

    sleep(0.5)
