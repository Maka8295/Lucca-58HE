# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

from time import sleep
import board
import adafruit_ds3502

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
ds3502 = adafruit_ds3502.DS3502(i2c)

# As this code runs, measure the voltage between ground and the RW (wiper) pin
# with a multimeter. You should see the voltage change with each print statement.
while True:
    ds3502.wiper = 127
    print("Wiper value set to 127")
    sleep(5.0)

    ds3502.wiper = 0
    print("Wiper value set to 0")
    sleep(5.0)

    ds3502.wiper = 63
    print("Wiper value set to 63")
    sleep(5.0)
