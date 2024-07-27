# SPDX-FileCopyrightText: 2020 by Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import board
import adafruit_bme280
import adafruit_sgp40

# Boards i2c bus
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sgp = adafruit_sgp40.SGP40(i2c)

# Humidity sensor for compensated Readings
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

while True:
    temperature = bme280.temperature
    humidity = bme280.relative_humidity

    # For compensated raw gas readings
    """
    compensated_raw_gas = sgp.measure_raw(
        temperature=temperature, relative_humidity=humidity
    )
    print("Raw Data:", compensated_raw_gas)
    """

    # For Compensated voc index readings
    # The algorithm expects a 1 hertz sampling rate. Run "measure index" once per second.
    # It may take several minutes for the VOC index to start changing
    # as it calibrates the baseline readings.
    voc_index = sgp.measure_index(temperature=temperature, relative_humidity=humidity)

    print("VOC Index:", voc_index)
    print("")
    time.sleep(1)
