# SPDX-FileCopyrightText: 2022 Tod Kurt for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example solicits notifications from Apple devices paired with it,
detecting specifically the IncomingCall and ActiveCall notification categories
and sending back Positive Actions to accept calls or Negative Actions to
decline or hang up calls. It also shows initiating pairing, prints existing
notifications and prints any new ones as they arrive.
"""

import time
import board
import digitalio
import neopixel
import adafruit_ble
from adafruit_ble.advertising.standard import SolicitServicesAdvertisement
import adafruit_ble_apple_notification_center as ancs

# Circuit Playground Bluefruit buttons and LED setup
butA = digitalio.DigitalInOut(board.D4)  # CPB "A" button
butB = digitalio.DigitalInOut(board.D5)  # CPB "B" button
butA.switch_to_input(digitalio.Pull.DOWN)  # buttons are active HIGH
butB.switch_to_input(digitalio.Pull.DOWN)

leds = neopixel.NeoPixel(board.D8, 10, brightness=0.1)

(coff, cred, cgrn, cblu, cgra) = (0x000000, 0xFF0000, 0x00FF00, 0x0000FF, 0x111111)
leds_off = (coff, coff, coff, coff, coff, coff, coff, coff, coff, coff)
leds_idle = (cgra, cgra, cgra, cgra, cgra, cgra, cgra, cgra, cgra, cgra)
leds_incoming_call = (coff, cgrn, cgrn, cgrn, coff, coff, cred, cred, cred, coff)
leds_active_call = (cgrn, coff, coff, coff, cgrn, cgrn, cred, cred, cred, cgrn)

print("starting...")
radio = adafruit_ble.BLERadio()  # pylint: disable=no-member
a = SolicitServicesAdvertisement()
# a.complete_name = "CIRPYCALLHANDLER" # this crashes things?
a.solicited_services.append(ancs.AppleNotificationCenterService)
radio.start_advertising(a)

last_display_time = time.monotonic()

while True:
    while not radio.connected:
        print("not connected")
        time.sleep(1)

    for connection in radio.connections:
        if not connection.paired:
            connection.pair()
            print("paired")

        ans = connection[ancs.AppleNotificationCenterService]

        for notification in ans.wait_for_new_notifications():
            print("New Notification:\n- ", notification)

        leds[:] = leds_idle

        for notification in ans.active_notifications.values():
            # incoming call category, has positive & negative actions
            if notification.category_id == 1:
                leds[:] = leds_incoming_call
                if butA.value:
                    print("Action: accepting call")
                    notification.send_positive_action()
                    time.sleep(1)  # simple debounce
                if butB.value:
                    print("Action: declining call")
                    notification.send_negative_action()
                    time.sleep(1)  # simple debounce
            # active call category, only has negative action
            if notification.category_id == 12:
                leds[:] = leds_active_call
                if butB.value:
                    print("Action: hanging up call")
                    notification.send_negative_action()
                    time.sleep(1)  # simple debounce

        if time.monotonic() - last_display_time > 3.0:
            last_display_time = time.monotonic()
            print(
                "Current Notifications:",
                len(ans.active_notifications),
                time.monotonic(),
            )
            for nid, n in ans.active_notifications.items():
                print(
                    "- uid:",
                    n.id,
                    "catid:",
                    n.category_id,
                    "title:",
                    n.title,
                    "msg:",
                    n.message,
                )
