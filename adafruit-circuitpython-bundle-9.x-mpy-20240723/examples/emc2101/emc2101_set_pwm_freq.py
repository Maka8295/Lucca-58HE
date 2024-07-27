# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import time
import board
from adafruit_emc2101.emc2101_lut import EMC2101_LUT as EMC2101

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

emc = EMC2101(i2c)
emc.set_pwm_clock(use_preset=False)
# Datasheet recommends using the maximum value of 31 (0x1F)
# to provide the highest effective resolution.
# The PWM frequency must be set before changing `manual_fan_speed` or LUT entries.
# Otherwise the PWM duty cycle won't be configured correctly.
emc.pwm_frequency = 14

# This divides the pwm frequency down to a smaller number
# so larger divisor = lower frequency
emc.pwm_frequency_divisor = 127

while True:
    print("External temperature:", emc.external_temperature, "C")
    emc.manual_fan_speed = 50
    time.sleep(1.5)
    print("Fan speed:", emc.fan_speed, "RPM")
    time.sleep(1)
