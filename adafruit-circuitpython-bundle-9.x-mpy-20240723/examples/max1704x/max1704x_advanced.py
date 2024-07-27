# SPDX-FileCopyrightText: Copyright (c) 2022 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time
import board
import adafruit_max1704x

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
max17 = adafruit_max1704x.MAX17048(i2c)

print(
    "Found MAX1704x with chip version",
    hex(max17.chip_version),
    "and id",
    hex(max17.chip_id),
)

# Quick starting allows an instant 'auto-calibration' of the battery. However, its a bad idea
# to do this right when the battery is first plugged in or if there's a lot of load on the battery
# so uncomment only if you're sure you want to 'reset' the chips charge calculator.
# print("Quick starting")
max17.quick_start = True

# The reset voltage is what the chip considers 'battery has been removed and replaced'
# The default is 3.0 Volts but you can change it here:
# max17.reset_voltage = 2.5
print("MAX1704x reset voltage = %0.1f V" % max17.reset_voltage)

# The analog comparator is used to detect the rest voltage, if you don't think the battery
# will ever be removed this can reduce current usage (see datasheet on VRESET.Dis)
print("Analog comparator is ", end="")
if max17.comparator_disabled:
    print("disabled")
else:
    print("enabled")

# Hibernation mode reduces how often the ADC is read, for power reduction. There is an automatic
# enter/exit mode but you can also customize the activity threshold both as voltage and charge rate
# max17.activity_threshold = 0.15
print("MAX1704x activity threshold = %0.2f V" % max17.activity_threshold)

# max17.hibernation_threshold = 5
print("MAX1704x hibernation threshold = %0.2f %%" % max17.hibernation_threshold)

# You can also 'force' hibernation mode!
# max17.hibernate()
# ...or force it to wake up!
# max17.wake()

# The alert pin can be used to detect when the voltage of the battery goes below or
# above a voltage, you can also query the alert in the loop.
max17.voltage_alert_min = 3.5
print("Voltage alert minimum = %0.2f V" % max17.voltage_alert_min)
max17.voltage_alert_max = 4.1
print("Voltage alert maximum = %0.2f V" % max17.voltage_alert_max)

print("")
while True:
    print(f"Battery voltage: {max17.cell_voltage:.2f} Volts")
    print(f"Battery state  : {max17.cell_percent:.1f} %")

    # we can check if we're hibernating or not
    if max17.hibernating:
        print("Hibernating!")

    if max17.active_alert:
        print("Alert!")
        if max17.reset_alert:
            print("  Reset indicator")
            max17.reset_alert = False  # clear the alert

        if max17.voltage_high_alert:
            print("  Voltage high")
            max17.voltage_high_alert = False  # clear the alert

        if max17.voltage_low_alert:
            print("  Voltage low")
            max17.voltage_low_alert = False  # clear the alert

        if max17.voltage_reset_alert:
            print("  Voltage reset")
            max17.voltage_reset_alert = False  # clear the alert

        if max17.SOC_low_alert:
            print("  Charge low")
            max17.SOC_low_alert = False  # clear the alert

        if max17.SOC_change_alert:
            print("  Charge changed")
            max17.SOC_change_alert = False  # clear the alert
    print("")
    time.sleep(1)
