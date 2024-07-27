# SPDX-FileCopyrightText: Copyright (c) 2024 Liz Clark for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_s35710

i2c = board.I2C()

timer = adafruit_s35710.Adafruit_S35710(i2c)

timer.alarm = 5
print(f"The S-35710 alarm is set for {timer.alarm} seconds")

countdown = timer.alarm - timer.clock

while True:
    print(f"The S-35710 clock is {timer.clock}")
    countdown = timer.alarm - timer.clock
    if countdown == 0:
        timer.alarm = 5
        print("Alarm reached! Resetting..")
    else:
        print(f"The alarm will expire in {countdown} seconds")
    time.sleep(1)
