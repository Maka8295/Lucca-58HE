# SPDX-FileCopyrightText: 2021 Dan Halbert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time

import adafruit_ble
from adafruit_ble.advertising.standard import Advertisement
from adafruit_ble_lywsd03mmc import LYWSD03MMCService

# PyLint can't find BLERadio for some reason so special case it here.
ble = adafruit_ble.BLERadio()  # pylint: disable=no-member

connection = None

while True:
    print("Scanning...")
    for adv in ble.start_scan(Advertisement, timeout=5):
        if adv.complete_name == "LYWSD03MMC":
            connection = ble.connect(adv)
            print("Connected")
            break

    # Stop scanning whether or not we are connected.
    ble.stop_scan()

    if connection and connection.connected:
        service = connection[LYWSD03MMCService]
        while connection.connected:
            print(
                "Temperature, Humidity",
                service.temperature_humidity,
            )
            time.sleep(5)
