# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import struct
import board
import adafruit_lsm6ds
import adafruit_lis3mdl
import adafruit_apds9960.apds9960
import adafruit_sht31d
import adafruit_bmp280
import adafruit_rockblock

# RockBlock setup
uart = board.UART()
uart.baudrate = 19200
rb = adafruit_rockblock.RockBlock(uart)

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

# all the sensors
accelo = adafruit_lsm6ds.LSM6DS33(i2c)
magno = adafruit_lis3mdl.LIS3MDL(i2c)
prox = adafruit_apds9960.apds9960.APDS9960(i2c)
sht = adafruit_sht31d.SHT31D(i2c)
bmp = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

# build data
# can decode on other end with struct.unpack("<6fB5f", data)
data = struct.pack("3f", *accelo.acceleration)
data += struct.pack("3f", *magno.magnetic)
data += struct.pack("B", prox.proximity())
data += struct.pack("2f", sht.relative_humidity, sht.temperature)
data += struct.pack("3f", bmp.pressure, bmp.altitude, bmp.temperature)

# send data
rb.data_out = data
print("Talking to satellite...")
retry = 0
status = rb.satellite_transfer()
while status[0] > 8:
    time.sleep(10)
    status = rb.satellite_transfer()
    print(retry, status)
    retry += 1
print("\nDONE.")
