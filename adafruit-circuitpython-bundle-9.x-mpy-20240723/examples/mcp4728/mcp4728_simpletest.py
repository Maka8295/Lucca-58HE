# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import adafruit_mcp4728

MCP4728_DEFAULT_ADDRESS = 0x60
MCP4728A4_DEFAULT_ADDRESS = 0x64

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
#  use for MCP4728 variant
mcp4728 = adafruit_mcp4728.MCP4728(i2c, adafruit_mcp4728.MCP4728_DEFAULT_ADDRESS)
#  use for MCP4728A4 variant
#  mcp4728 = adafruit_mcp4728.MCP4728(i2c, adafruit_mcp4728.MCP4728A4_DEFAULT_ADDRESS)

mcp4728.channel_a.value = 65535  # Voltage = VDD
mcp4728.channel_b.value = int(65535 / 2)  # VDD/2
mcp4728.channel_c.value = int(65535 / 4)  # VDD/4
mcp4728.channel_d.value = 0  # 0V
