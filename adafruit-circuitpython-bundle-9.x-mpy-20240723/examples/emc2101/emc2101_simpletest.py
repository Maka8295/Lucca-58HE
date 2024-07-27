# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import time
import board
from adafruit_emc2101 import EMC2101

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
emc = EMC2101(i2c)
while True:
    print("Setting fan speed to 25%")
    emc.manual_fan_speed = 25
    time.sleep(2)  # longer sleep to let it spin down from 100%
    print("Fan speed", emc.fan_speed)
    time.sleep(1)

    print("Setting fan speed to 50%")
    emc.manual_fan_speed = 50
    time.sleep(1.5)
    print("Fan speed", emc.fan_speed)
    time.sleep(1)

    print("Setting fan speed to 75%")
    emc.manual_fan_speed = 75
    time.sleep(1.5)
    print("Fan speed", emc.fan_speed)
    time.sleep(1)

    print("Setting fan speed to 100%")
    emc.manual_fan_speed = 100
    time.sleep(1.5)
    print("Fan speed", emc.fan_speed)
    time.sleep(1)

    print("External temperature:", emc.external_temperature, "C")
    print("Internal temperature:", emc.internal_temperature, "C")

    print("")
    time.sleep(0.5)
