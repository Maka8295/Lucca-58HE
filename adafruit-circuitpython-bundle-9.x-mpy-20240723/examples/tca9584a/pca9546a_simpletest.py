# SPDX-FileCopyrightText: 2021 Carter Nelson for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example shows using TCA9548A to perform a simple scan for connected devices
import board
import adafruit_tca9548a

# Create I2C bus as normal
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

# Create the PCA9546A object and give it the I2C bus
mux = adafruit_tca9548a.PCA9546A(i2c)

for channel in range(4):
    if mux[channel].try_lock():
        print("Channel {}:".format(channel), end="")
        addresses = mux[channel].scan()
        print([hex(address) for address in addresses if address != 0x70])
        mux[channel].unlock()
