# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time

import adafruit_ble
from adafruit_ble_adafruit.adafruit_service import AdafruitServerAdvertisement
from adafruit_ble_adafruit.temperature_service import TemperatureService

# PyLint can't find BLERadio for some reason so special case it here.
ble = adafruit_ble.BLERadio()  # pylint: disable=no-member

connection = None

while True:
    print("Scanning for an Adafruit Server advertisement...")
    for adv in ble.start_scan(AdafruitServerAdvertisement, timeout=5):
        connection = ble.connect(adv)
        print("Connected")
        break

    # Stop scanning whether or not we are connected.
    ble.stop_scan()

    if connection and connection.connected:
        temp_service = connection[TemperatureService]
        while connection.connected:
            print("Temperature:", temp_service.temperature)
            time.sleep(1)
