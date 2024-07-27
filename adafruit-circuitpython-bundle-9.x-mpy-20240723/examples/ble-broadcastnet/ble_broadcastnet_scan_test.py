# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This example merely scans for broadcastnet packets to check that something is sending them."""

import adafruit_ble
import adafruit_ble_broadcastnet

ble = adafruit_ble.BLERadio()

print("scanning")
# By providing Advertisement as well we include everything, not just specific advertisements.
for advert in ble.start_scan(
    adafruit_ble_broadcastnet.AdafruitSensorMeasurement, interval=0.5
):
    print(advert)
