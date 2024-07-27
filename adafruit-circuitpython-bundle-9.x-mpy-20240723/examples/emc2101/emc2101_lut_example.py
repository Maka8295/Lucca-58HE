# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import time
import board
from adafruit_emc2101.emc2101_lut import EMC2101_LUT as EMC2101

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

FAN_MAX_RPM = 1700
emc = EMC2101(i2c)
emc.manual_fan_speed = 50
time.sleep(1)
emc.lut[27] = 25
emc.lut[34] = 50
emc.lut[42] = 75
emc.lut_enabled = True
emc.forced_temp_enabled = True
print("Lut:", emc.lut)
emc.forced_ext_temp = 28  # over 25, should be 25%
time.sleep(3)
print("25%% duty cycle is %f RPM:" % emc.fan_speed)


emc.forced_ext_temp = 35  # over 30, should be 50%
time.sleep(3)
print("50%% duty cycle is %f RPM:" % emc.fan_speed)

emc.forced_ext_temp = 43  # over 42, should be 75%
time.sleep(3)
print("75%% duty cycle is %f RPM:" % emc.fan_speed)
