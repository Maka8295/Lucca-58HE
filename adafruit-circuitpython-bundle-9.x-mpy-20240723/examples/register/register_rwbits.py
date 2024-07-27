# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

from board import SCL, SDA
from busio import I2C
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register.i2c_bits import RWBits

DEVICE_ADDRESS = 0x39  # device address of APDS9960 board
A_DEVICE_REGISTER_1 = 0xA2  # a control register on the APDS9960 board
A_DEVICE_REGISTER_2 = 0xA3  # another control register on the APDS9960 board


class DeviceControl:  # pylint: disable-msg=too-few-public-methods
    def __init__(self, i2c):
        self.i2c_device = i2c  # self.i2c_device required by RWBit class

    setting1 = RWBits(2, A_DEVICE_REGISTER_1, 6)  # 2 bits: bits 6 & 7
    setting2 = RWBits(2, A_DEVICE_REGISTER_2, 5)  # 2 bits: bits 5 & 6


# The follow is for I2C communications
comm_port = I2C(SCL, SDA)
device = I2CDevice(comm_port, DEVICE_ADDRESS)
settings = DeviceControl(device)

# set the bits in the device
settings.setting1 = 0
settings.setting2 = 3
# display the device values for the bits
print("setting1: {}; setting2: {}".format(settings.setting1, settings.setting2))

# toggle the bits
settings.setting1 = 3
settings.setting2 = 0
# display the device values for the bits
print("setting1: {}; setting2: {}".format(settings.setting1, settings.setting2))
