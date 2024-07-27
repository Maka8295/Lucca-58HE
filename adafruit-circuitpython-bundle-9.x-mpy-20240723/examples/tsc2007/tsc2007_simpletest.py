# SPDX-FileCopyrightText: Copyright (c) 2022 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense


import board
import adafruit_tsc2007

# Use for I2C
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

irq_dio = None  # don't use an irq pin by default
# uncomment for optional irq input pin so we don't continuously poll the I2C for touches
# irq_dio = digitalio.DigitalInOut(board.A0)
tsc = adafruit_tsc2007.TSC2007(i2c, irq=irq_dio)

while True:
    if tsc.touched:
        point = tsc.touch
        if point["pressure"] < 100:  # ignore touches with no 'pressure' as false
            continue
        print("Touchpoint: (%d, %d, %d)" % (point["x"], point["y"], point["pressure"]))
