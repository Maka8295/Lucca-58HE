# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

from board import SCL, SDA
from busio import I2C
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register.i2c_struct import Struct

DEVICE_ADDRESS = 0x40  # device address of PCA9685 board
A_DEVICE_REGISTER = 0x06  # PWM 0 control register on the PCA9685 board


class DeviceControl:  # pylint: disable-msg=too-few-public-methods
    def __init__(self, i2c):
        self.i2c_device = i2c  # self.i2c_device required by Struct class

    tuple_of_numbers = Struct(A_DEVICE_REGISTER, "<HH")  # 2 16-bit numbers


# The follow is for I2C communications
comm_port = I2C(SCL, SDA)
device = I2CDevice(comm_port, DEVICE_ADDRESS)
registers = DeviceControl(device)

# set the bits in the device
registers.tuple_of_numbers = (0, 0x00FF)
# display the device values for the bits
print("register 1: {}; register 2: {}".format(*registers.tuple_of_numbers))

# toggle the bits
registers.tuple_of_numbers = (0x1000, 0)
# display the device values for the bits
print("register 1: {}; register 2: {}".format(*registers.tuple_of_numbers))
