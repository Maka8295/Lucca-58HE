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
# max17.quick_start = True

while True:
    print(f"Battery voltage: {max17.cell_voltage:.2f} Volts")
    print(f"Battery state  : {max17.cell_percent:.1f} %")
    print("")
    time.sleep(1)
