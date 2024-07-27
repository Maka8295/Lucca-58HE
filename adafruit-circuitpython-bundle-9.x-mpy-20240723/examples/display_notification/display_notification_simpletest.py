# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This demo shows the latest notification from a connected Apple device on a TFT Gizmo screen.

The A and B buttons on the CircuitPlayground Bluefruit can be used to scroll through all active
notifications.
"""

import time
import board
import digitalio
import displayio
import adafruit_ble
from adafruit_ble.advertising.standard import SolicitServicesAdvertisement

from adafruit_ble_apple_notification_center import AppleNotificationCenterService
from adafruit_display_ble_status.advertising import AdvertisingWidget
from adafruit_gizmo import tft_gizmo
from adafruit_display_notification import apple
from adafruit_display_notification import NotificationFree

# from adafruit_circuitplayground import cp

# This is a whitelist of apps to show notifications from.
# APPS = ["com.tinyspeck.chatlyio", "com.atebits.Tweetie2"]
APPS = []

DELAY_AFTER_PRESS = 15
DEBOUNCE = 0.1

a = digitalio.DigitalInOut(board.BUTTON_A)
a.switch_to_input(pull=digitalio.Pull.DOWN)
b = digitalio.DigitalInOut(board.BUTTON_B)
b.switch_to_input(pull=digitalio.Pull.DOWN)


def find_connection():
    for connection in radio.connections:
        if AppleNotificationCenterService not in connection:
            continue
        if not connection.paired:
            connection.pair()
        return connection, connection[AppleNotificationCenterService]
    return None, None


# Start advertising before messing with the display so that we can connect immediately.
radio = adafruit_ble.BLERadio()
advertisement = SolicitServicesAdvertisement()
advertisement.solicited_services.append(AppleNotificationCenterService)

SCALE = 2

display = tft_gizmo.TFT_Gizmo()
group = displayio.Group(scale=SCALE)
display.root_group = group

width = display.width // SCALE
height = display.height // SCALE

radio_widget = AdvertisingWidget("CIRCUITPY", width, height)
group.append(radio_widget)

current_notification = None
all_ids = []
last_press = time.monotonic()
active_connection, notification_service = find_connection()
while True:
    if not active_connection:
        radio.start_advertising(advertisement)

    while not active_connection:
        active_connection, notification_service = find_connection()

    while active_connection.connected:
        all_ids.clear()
        current_notifications = notification_service.active_notifications
        for notification_id in current_notifications:
            notification = current_notifications[notification_id]
            if APPS and notification.app_id not in APPS:
                continue
            all_ids.append(notification_id)

        # For now, use _raw_date even though we should use a parsed version of the date.
        # pylint: disable=protected-access
        all_ids.sort(key=lambda x: current_notifications[x]._raw_date)

        if current_notification and current_notification.removed:
            # Stop showing the latest and show that there are no new notifications.
            current_notification = None

        if not current_notification and not all_ids:
            group[0] = NotificationFree(width, height)
        elif all_ids:
            now = time.monotonic()
            if (
                current_notification
                and current_notification.id in all_ids
                and now - last_press < DELAY_AFTER_PRESS
            ):
                index = all_ids.index(current_notification.id)
            else:
                index = len(all_ids) - 1
            if now - last_press >= DEBOUNCE:
                if b.value and index > 0:
                    last_press = now
                    index += -1
                if a.value and index < len(all_ids) - 1:
                    last_press = now
                    index += 1

            notification_id = all_ids[index]
            if not current_notification or current_notification.id != notification_id:
                current_notification = current_notifications[notification_id]
                print(current_notification._raw_date, current_notification)
                group[0] = apple.create_notification_widget(
                    current_notification, width, height
                )

    active_connection = None
    notification_service = None
