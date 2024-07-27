# SPDX-FileCopyrightText: 2023 Liz Clark for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo to read analog input on channel 0

import time
import board
import adafruit_ads7830.ads7830 as ADC
from adafruit_ads7830.analog_in import AnalogIn

i2c = board.I2C()

# Initialize ADS7830
adc = ADC.ADS7830(i2c)
chan = AnalogIn(adc, 0)

while True:
    print(f"ADC channel 0 = {chan.value}")
    time.sleep(0.1)
