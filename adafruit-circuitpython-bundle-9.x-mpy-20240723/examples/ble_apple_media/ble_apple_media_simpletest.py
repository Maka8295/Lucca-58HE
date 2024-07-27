# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example solicits that apple devices that provide notifications connect to it, initiates
pairing, prints existing notifications and then prints any new ones as they arrive.
"""

import time
import adafruit_ble
from adafruit_ble.advertising.standard import SolicitServicesAdvertisement
from adafruit_ble_apple_media import AppleMediaService

# PyLint can't find BLERadio for some reason so special case it here.
radio = adafruit_ble.BLERadio()  # pylint: disable=no-member
a = SolicitServicesAdvertisement()
a.solicited_services.append(AppleMediaService)
radio.start_advertising(a)

while not radio.connected:
    pass

print("connected")

known_notifications = set()

i = 0
while radio.connected:
    for connection in radio.connections:
        if not connection.paired:
            connection.pair()
            print("paired")

        ams = connection[AppleMediaService]
        print("App:", ams.player_name)
        print("Title:", ams.title)
        print("Album:", ams.album)
        print("Artist:", ams.artist)
        if ams.playing:
            print("Playing")
        elif ams.paused:
            print("Paused")

        if i > 3:
            ams.toggle_play_pause()
            i = 0
    print()
    time.sleep(3)
    i += 1

print("disconnected")
