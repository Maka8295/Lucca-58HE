# SPDX-FileCopyrightText: Copyright (c) 2022 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time
import board
import adafruit_ens160

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

ens = adafruit_ens160.ENS160(i2c)
print("Firmware Vers: ", ens.firmware_version)

ens.mode = adafruit_ens160.MODE_STANDARD
curr_mode = ens.mode
print("Current mode: ", end="")
if curr_mode == adafruit_ens160.MODE_SLEEP:
    print("Sleeping")
if curr_mode == adafruit_ens160.MODE_IDLE:
    print("Idle")
if curr_mode == adafruit_ens160.MODE_STANDARD:
    print("Standard sensing")

# Set the temperature compensation variable to the ambient temp
# for best sensor calibration
ens.temperature_compensation = 25
print("Current temperature compensation = %0.1f *C" % ens.temperature_compensation)
# Same for ambient relative humidity
ens.humidity_compensation = 50
print("Current rel humidity compensation = %0.1f %%" % ens.humidity_compensation)
print()

# We can have the INT pin tell us when new data is available
ens.interrupt_pushpull = True  # use pushpull 3V, not open-drain
ens.interrupt_on_data = True  # Tell us when there's new calculated data
ens.interrupt_polarity = False  # Active 'low' (false)
ens.interrupt_enable = True  # enable pin

while True:
    # if no data, loop over
    if not ens.new_data_available:
        time.sleep(0.1)
        continue

    # Check status
    status = ens.data_validity
    if status == adafruit_ens160.NORMAL_OP:
        print("Normal operation")
    if status == adafruit_ens160.WARM_UP:
        print("Warming up")
    if status == adafruit_ens160.START_UP:
        print("Initial startup")
    if status == adafruit_ens160.INVALID_OUT:
        print("Invalid output")

    # read all sensors at once and print out the structure
    data = ens.read_all_sensors()
    print("AQI (1-5):", data["AQI"])
    print("TVOC (ppb):", data["TVOC"])
    print("eCO2 (ppm):", data["eCO2"])
    print("Sensor resistances (ohms):", data["Resistances"])
    print()
