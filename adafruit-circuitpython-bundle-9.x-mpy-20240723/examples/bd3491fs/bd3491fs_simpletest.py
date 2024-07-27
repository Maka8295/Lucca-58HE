# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import busio
import adafruit_bd3491fs

i2c = busio.I2C(board.SCL, board.SDA)
bd3491fs = adafruit_bd3491fs.BD3491FS(i2c)

bd3491fs.active_input = adafruit_bd3491fs.Input.A
bd3491fs.input_gain = adafruit_bd3491fs.Level.LEVEL_20DB
bd3491fs.channel_1_attenuation = 0
bd3491fs.channel_2_attenuation = 0
