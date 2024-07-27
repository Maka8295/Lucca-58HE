# SPDX-FileCopyrightText: 2020 Eva Herrada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example solicits that apple devices that provide notifications connect to it, initiates
pairing, then allows the user to use a CLUE board as a media remote through both the buttons
and capacitive touch pads.

This example requires the following additional libraries:
adafruit_ble
adafruit_ble_apple_media
"""

import time
import adafruit_ble
from adafruit_ble.advertising.standard import SolicitServicesAdvertisement
from adafruit_ble_apple_media import AppleMediaService
from adafruit_clue import clue

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
if radio.connected:
    for connection in radio.connections:
        if not connection.paired:
            connection.pair()
            print("paired")

        ams = connection[AppleMediaService]

while radio.connected:
    if ams.playing:
        play_str = "Playing"
    else:
        play_str = "Paused"
    print("{} - {},  {}".format(ams.title, ams.artist, play_str))

    # Capacitive touch pad marked 0 goes to the previous track
    if clue.touch_0:
        ams.previous_track()
        time.sleep(0.25)

    # Capacitive touch pad marked 1 toggles pause/play
    if clue.touch_1:
        ams.toggle_play_pause()
        time.sleep(0.25)

    # Capacitive touch pad marked 2 advances to the next track
    if clue.touch_2:
        ams.next_track()
        time.sleep(0.25)

    # If button B (on the right) is pressed, it increases the volume
    if clue.button_b:
        ams.volume_up()
        time.sleep(0.30)
        while clue.button_b:
            ams.volume_up()
            time.sleep(0.07)

    # If button A (on the left) is pressed, the volume decreases
    if clue.button_a:
        ams.volume_down()
        time.sleep(0.30)
        while clue.button_a:
            ams.volume_down()
            time.sleep(0.07)

print("disconnected")
