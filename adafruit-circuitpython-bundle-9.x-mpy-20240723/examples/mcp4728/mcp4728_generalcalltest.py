# SPDX-FileCopyrightText: 2021 codenio (Aananth K)
# SPDX-License-Identifier: MIT

import board
import adafruit_mcp4728

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
mcp4728 = adafruit_mcp4728.MCP4728(i2c)

mcp4728.channel_a.value = 65535  # Voltage = VDD
mcp4728.channel_b.value = int(65535 / 2)  # VDD/2
mcp4728.channel_c.value = int(65535 / 4)  # VDD/4
mcp4728.channel_d.value = 0  # 0V

mcp4728.save_settings()  # save current voltages into EEPROM

print("Settings Saved into EEPROM")

input("Press Enter to modify the channel outputs...")

mcp4728.channel_a.value = 0  # Modify output
mcp4728.channel_b.value = 0  # Modify output
mcp4728.channel_c.value = 0  # Modify output
mcp4728.channel_d.value = 65535  # Modify output

print("Channel Outputs Modified")

input("Press Enter to invoke General Call Reset ...")

mcp4728.reset()  # reset MCP4728
