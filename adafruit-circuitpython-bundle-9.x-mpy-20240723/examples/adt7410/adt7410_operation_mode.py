# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
import board
import adt7410

i2c = board.I2C()
adt = adt7410.ADT7410(i2c)

adt.operation_mode = adt7410.SPS

while True:
    for operation_mode in adt7410.operation_mode_values:
        print("Current Operation mode setting: ", adt.operation_mode)
        for _ in range(10):
            print("Temperature: {:.2f}C".format(adt.temperature))
            time.sleep(0.5)
        adt.operation_mode = operation_mode
