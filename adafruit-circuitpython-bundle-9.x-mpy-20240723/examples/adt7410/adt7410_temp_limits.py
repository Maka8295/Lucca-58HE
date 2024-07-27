# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adt7410

i2c = board.I2C()  # uses board.SCL and board.SDA
adt = adt7410.ADT7410(i2c)

adt.low_temperature = 18
adt.high_temperature = 29
adt.critical_temperature = 35
adt.hysteresis_temperature = 2

print("High limit: {}C".format(adt.high_temperature))
print("Low limit: {}C".format(adt.low_temperature))
print("Critical limit: {}C".format(adt.critical_temperature))

adt.comparator_mode = adt7410.COMP_ENABLED

while True:
    print("Temperature: {:.2f}C".format(adt.temperature))
    alert_status = adt.alert_status
    if alert_status.high_alert:
        print("Temperature above high set limit!")
    if alert_status.low_alert:
        print("Temperature below low set limit!")
    if alert_status.critical_alert:
        print("Temperature above critical set limit!")
    time.sleep(1)
