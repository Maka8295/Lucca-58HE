# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This is a complex sensor node that uses the sensors on a Clue and Feather Bluefruit Sense."""

import time
import board
import adafruit_bmp280
import adafruit_sht31d

# import adafruit_apds9960.apds9960
import adafruit_lis3mdl
import adafruit_lsm6ds
import adafruit_ble_broadcastnet

print("This is BroadcastNet sensor:", adafruit_ble_broadcastnet.device_address)

i2c = board.I2C()

# Define sensors:
# Accelerometer/gyroscope:
lsm6ds = adafruit_lsm6ds.LSM6DS33(i2c)

# Magnetometer:
lis3mdl = adafruit_lis3mdl.LIS3MDL(i2c)

# DGesture/proximity/color/light sensor:
# TODO: How do we get the light level?
# apds9960 = adafruit_apds9960.apds9960.APDS9960(i2c)
# apds9960.enable_color = True

# Humidity sensor:
sht31d = adafruit_sht31d.SHT31D(i2c)

# Barometric pressure sensor:
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

while True:
    measurement = adafruit_ble_broadcastnet.AdafruitSensorMeasurement()
    measurement.temperature = (sht31d.temperature, bmp280.temperature)
    measurement.relative_humidity = sht31d.relative_humidity
    measurement.pressure = bmp280.pressure
    measurement.acceleration = lsm6ds.acceleration
    measurement.magnetic = lis3mdl.magnetic
    print(measurement)
    adafruit_ble_broadcastnet.broadcast(measurement)
    time.sleep(60)
