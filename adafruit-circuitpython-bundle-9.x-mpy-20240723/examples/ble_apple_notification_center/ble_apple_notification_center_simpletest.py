# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example solicits that apple devices that provide notifications connect to it, initiates
pairing, and prints existing notifications.
"""

import adafruit_ble
from adafruit_ble.advertising.standard import SolicitServicesAdvertisement
import adafruit_ble_apple_notification_center as ancs

# PyLint can't find BLERadio for some reason so special case it here.
radio = adafruit_ble.BLERadio()  # pylint: disable=no-member
a = SolicitServicesAdvertisement()
a.solicited_services.append(ancs.AppleNotificationCenterService)
radio.start_advertising(a)

print("Waiting for connection")

while not radio.connected:
    pass

print("Connected")

for connection in radio.connections:
    if ancs.AppleNotificationCenterService not in connection:
        continue

    if not connection.paired:
        connection.pair()
        print("Paired")

    ans = connection[ancs.AppleNotificationCenterService]
    # Wait for the notifications to load.
    while len(ans.active_notifications) == 0:
        pass
    for notification_id in ans.active_notifications:
        notification = ans.active_notifications[notification_id]
        print(notification.app_id, notification.title)
