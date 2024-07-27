# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example solicits that apple devices that provide notifications connect to it, initiates
pairing, prints existing notifications and then prints any new ones as they arrive.
"""

import time
import adafruit_ble
from adafruit_ble.advertising.standard import SolicitServicesAdvertisement
import adafruit_ble_apple_notification_center as ancs

# PyLint can't find BLERadio for some reason so special case it here.
radio = adafruit_ble.BLERadio()  # pylint: disable=no-member
a = SolicitServicesAdvertisement()
a.solicited_services.append(ancs.AppleNotificationCenterService)
radio.start_advertising(a)

while not radio.connected:
    pass

print("connected")

known_notifications = set()

while radio.connected:
    for connection in radio.connections:
        if not connection.paired:
            connection.pair()
            print("paired")

        ans = connection[ancs.AppleNotificationCenterService]
        for notification in ans.wait_for_new_notifications():
            print(notification)

        print(len(ans.active_notifications))
    time.sleep(1)

print("disconnected")
