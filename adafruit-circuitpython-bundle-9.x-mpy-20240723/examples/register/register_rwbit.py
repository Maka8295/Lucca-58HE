# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

from board import SCL, SDA
from busio import I2C
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register.i2c_bit import RWBit

DEVICE_ADDRESS = 0x68  # device address of DS3231 board
A_DEVICE_REGISTER = 0x0E  # control register on the DS3231 board


class DeviceControl:  # pylint: disable-msg=too-few-public-methods
    def __init__(self, i2c):
        self.i2c_device = i2c  # self.i2c_device required by RWBit class

    flag1 = RWBit(A_DEVICE_REGISTER, 0)  # bit 0 of the control register
    flag2 = RWBit(A_DEVICE_REGISTER, 1)  # bit 1
    flag3 = RWBit(A_DEVICE_REGISTER, 7)  # bit 7


# The follow is for I2C communications
comm_port = I2C(SCL, SDA)
device = I2CDevice(comm_port, DEVICE_ADDRESS)
flags = DeviceControl(device)

# set the bits in the device
flags.flag1 = False
flags.flag2 = True
flags.flag3 = False
# display the device values for the bits
print("flag1: {}; flag2: {}; flag3: {}".format(flags.flag1, flags.flag2, flags.flag3))

# toggle the bits
flags.flag1 = not flags.flag1
flags.flag2 = not flags.flag2
flags.flag3 = not flags.flag3
# display the device values for the bits
print("flag1: {}; flag2: {}; flag3: {}".format(flags.flag1, flags.flag2, flags.flag3))
