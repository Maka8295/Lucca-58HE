# SPDX-FileCopyrightText: Copyright (c) 2024 Liz Clark for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_adg72x

i2c = board.I2C()
switch = adafruit_adg72x.ADG72x(i2c)

count = 0

while True:
    print(f"Selecting channel {count}")
    switch.channel = count
    count = (count + 1) % 8
    time.sleep(1)
