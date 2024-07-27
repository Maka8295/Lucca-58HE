# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Alec Delaney for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time
from adafruit_ble import BLERadio
from adafruit_ble_beacon import iBeaconAdvertisement

ble = BLERadio()

while True:
    for entry in ble.start_scan(iBeaconAdvertisement, minimum_rssi=-120, timeout=3):
        print("Beacon Power", entry.beacon_tx_power)
        print("UUID:", entry.uuid)
        print("Major", entry.major)
        print("Minor:", entry.minor)
        print("Distance:", entry.distance)
        time.sleep(1)
    time.sleep(3)
