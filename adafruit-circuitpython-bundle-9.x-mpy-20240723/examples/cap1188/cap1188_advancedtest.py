# SPDX-FileCopyrightText: 2021 Jose David M.
# SPDX-License-Identifier: MIT

# To use in the REPL >>> import cap1188_advancetest

import board
from adafruit_cap1188.i2c import CAP1188_I2C

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
cap = CAP1188_I2C(i2c)

print(f"Sensor Initial Configuration Values: {cap.averaging, cap.sample, cap.cycle}")

averages = (1, 2, 4, 8, 16, 32, 64, 128)
samples = ("320us", "640us", "1.28ms", "2.56ms")
cycles = ("35ms", "70ms", "105ms", "140ms")

print("Setting Up Averages")
for i in averages:
    cap.averaging = i
    print(f"Average: {cap.averaging}")

print("Setting Up Samples")
for i in samples:
    cap.sample = i
    print(f"Sample: {cap.sample}")

print("Setting Up Samples")
for i in cycles:
    cap.cycle = i
    print(f"Cycle: {cap.cycle}")

print("Done!")
