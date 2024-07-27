# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time
import board
import digitalio
import adafruit_pca9554

board.I2C().deinit()
i2c = board.I2C()
tft_io_expander = dict(board.TFT_IO_EXPANDER)

pcf = adafruit_pca9554.PCA9554(i2c, address=tft_io_expander["i2c_address"])
button_up = pcf.get_pin(board.BTN_UP)
button_up.switch_to_input(pull=digitalio.Pull.UP)

while True:
    print(button_up.value)
    time.sleep(0.01)  # debounce
