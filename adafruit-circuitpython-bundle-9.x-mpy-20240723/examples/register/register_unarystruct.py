# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

from board import SCL, SDA
from busio import I2C
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register.i2c_struct import UnaryStruct

DEVICE_ADDRESS = 0x74  # device address of PCA9685 board
A_DEVICE_REGISTER_1 = 0x00  # Configuration register on the is31fl3731 board
A_DEVICE_REGISTER_2 = 0x03  # Auto Play Control Register 2 on the is31fl3731 board


class DeviceControl:  # pylint: disable-msg=too-few-public-methods
    def __init__(self, i2c):
        self.i2c_device = i2c  # self.i2c_device required by UnaryStruct class

    register1 = UnaryStruct(A_DEVICE_REGISTER_1, "<B")  # 8-bit number
    register2 = UnaryStruct(A_DEVICE_REGISTER_2, "<B")  # 8-bit number


# The follow is for I2C communications
comm_port = I2C(SCL, SDA)
device = I2CDevice(comm_port, DEVICE_ADDRESS)
registers = DeviceControl(device)

# set the bits in the device
registers.register1 = 1 << 3 | 2
registers.register2 = 32
# display the device values for the bits
print("register 1: {}; register 2: {}".format(registers.register1, registers.register2))

# toggle the bits
registers.register1 = 2 << 3 | 5
registers.register2 = 60
# display the device values for the bits
print("register 1: {}; register 2: {}".format(registers.register1, registers.register2))
