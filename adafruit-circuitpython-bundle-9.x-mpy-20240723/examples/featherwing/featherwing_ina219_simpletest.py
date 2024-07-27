# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

""" Example to print out the voltage and current using the INA219 """
import time
from adafruit_featherwing import ina219_featherwing

INA219 = ina219_featherwing.INA219FeatherWing()

while True:
    print("Bus Voltage:   {} V".format(INA219.bus_voltage))
    print("Shunt Voltage: {} V".format(INA219.shunt_voltage))
    print("Voltage:       {} V".format(INA219.voltage))
    print("Current:       {} mA".format(INA219.current))
    print("")
    time.sleep(0.5)
