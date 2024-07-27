# SPDX-FileCopyrightText: Copyright (c) 2024 Liz Clark for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Adafruit DS248x DS18B20 Example"""

import time
import board
from adafruit_ds248x import Adafruit_DS248x

# Initialize I2C bus and DS248x
i2c = board.I2C()
ds248x = Adafruit_DS248x(i2c)

rom = bytearray(8)
if not ds248x.onewire_search(rom):
    print("No more devices found\n\n")

print("Found device ROM: ", end="")
for byte in rom:
    print(f"{byte:02X} ", end="")
print()
while True:
    temperature = ds248x.ds18b20_temperature(rom)
    print(f"Temperature: {temperature:.2f} °C")

    time.sleep(1)
