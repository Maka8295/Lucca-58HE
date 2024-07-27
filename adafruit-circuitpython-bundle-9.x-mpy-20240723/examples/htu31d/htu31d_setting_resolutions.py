# SPDX-FileCopyrightText: Copyright (c) 2021 Jose David M.
#
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_htu31d


# import htu31d_setting_resolutions
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
htu = adafruit_htu31d.HTU31D(i2c)


print("Temperature Resolution: ", htu.temp_resolution)
print("Humidity Resolution: ", htu.humidity_resolution)

# Setting the temperature resolution.
# Possible values are "0.040", "0.025", "0.016" and "0.012"
htu.temp_resolution = "0.040"

# Setting the Relative Humidity resolution.
# Possible values are "0.020%", "0.014%", "0.010%" and "0.007%"
htu.humidity_resolution = "0.020%"

print("Temperature Resolution: ", htu.temp_resolution)
print("Humidity Resolution: ", htu.humidity_resolution)

hum_res = ["0.020%", "0.014%", "0.010%", "0.007%"]
temp_res = ["0.040", "0.025", "0.016", "0.012"]

while True:
    for humidity_resolution in hum_res:
        htu.humidity_resolution = humidity_resolution
        print(f"Current Humidity Resolution: {humidity_resolution}")
        for _ in range(2):
            print(f"Humidity: {htu.relative_humidity:.2f}")
            print(f"Temperature: {htu.temperature:.2f}")
            print("")
            time.sleep(0.5)
    for temperature_resolution in temp_res:
        htu.temp_resolution = temperature_resolution
        print(f"Current Temperature Resolution: {temperature_resolution}")
        for _ in range(2):
            print(f"Humidity: {htu.relative_humidity:.2f}")
            print(f"Temperature: {htu.temperature:.2f}")
            print("")
            time.sleep(0.5)
