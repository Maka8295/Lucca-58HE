# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Analog to digital converter example.
# Will loop forever printing ADC channel 1 raw and mV values every second.
# NOTE the ADC can only read voltages in the range of ~900mV to 1800mV!

import time
import board
import busio
import adafruit_lis3dh

# Uncomment if using SPI
# import digitalio


# Hardware I2C setup. Use the CircuitPlayground built-in accelerometer if available;
# otherwise check I2C pins.
if hasattr(board, "ACCELEROMETER_SCL"):
    i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
    lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19)
else:
    i2c = board.I2C()  # uses board.SCL and board.SDA
    # i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
    lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c)

# Hardware SPI setup:
# spi = board.SPI()
# cs = digitalio.DigitalInOut(board.D5)  # Set to correct CS pin!
# lis3dh = adafruit_lis3dh.LIS3DH_SPI(spi, cs)

# PyGamer I2C Setup:
# i2c = board.I2C(A)  # uses board.SCL and board.SDA
# lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19)


# Loop forever printing ADC readings.
while True:
    # Read raw ADC value.  Specify which ADC to read: 1, 2, or 3.
    adc1_raw = lis3dh.read_adc_raw(1)
    # Or read the ADC value in millivolts:
    adc1_mV = lis3dh.read_adc_mV(1)
    print("ADC 1 = {} ({} mV)".format(adc1_raw, adc1_mV))
    time.sleep(1)
