# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This example broadcasts our Mac Address as our Eddystone ID and a link to the Adafruit Discord
   server."""

import time

import adafruit_ble
from adafruit_ble_eddystone import uid, url

radio = adafruit_ble.BLERadio()

# Reuse the BLE address as our Eddystone instance id.
eddystone_uid = uid.EddystoneUID(radio.address_bytes)
eddystone_url = url.EddystoneURL("https://adafru.it/discord")

while True:
    # Alternate between advertising our ID and our URL.
    radio.start_advertising(eddystone_uid)
    time.sleep(0.5)
    radio.stop_advertising()

    radio.start_advertising(eddystone_url)
    time.sleep(0.5)
    radio.stop_advertising()

    time.sleep(4)
