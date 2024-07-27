# SPDX-FileCopyrightText: 2020 Eva Herrada for Adafruit Industries
# SPDX-License-Identifier: MIT
""" This example solicits that apple devices that provide notifications connect to it, initiates
pairing, then allows the user to use a CLUE board as a media remote through both the buttons
and capacitive touch pads.

This example requires the following additional libraries:
adafruit_ble
adafruit_ble_apple_media
adafruit_bitmap_font
adafruit_display_shapes
adafruit_display_text

This example requires a lot of memory resources, make sure that you use
the mpy version of the libraries
"""

import time
import board
import displayio
from adafruit_display_text import label
import adafruit_ble
from adafruit_ble.advertising.standard import SolicitServicesAdvertisement
from adafruit_ble_apple_media import AppleMediaService
from adafruit_ble_apple_media import UnsupportedCommand
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.rect import Rect
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


# arial12 = bitmap_font.load_font("/fonts/Arial-12.bdf")
arial16 = bitmap_font.load_font("/fonts/Arial-16.bdf")
# arial24 = bitmap_font.load_font("/fonts/Arial-Bold-24.bdf")

display = board.DISPLAY

group = displayio.Group()

title = label.Label(font=arial16, x=15, y=25, text="_", color=0xFFFFFF)
group.append(title)

artist = label.Label(font=arial16, x=15, y=50, text="_", color=0xFFFFFF)
group.append(artist)

album = label.Label(font=arial16, x=15, y=75, text="_", color=0xFFFFFF)
group.append(album)

player = label.Label(font=arial16, x=15, y=100, text="_", color=0xFFFFFF)
group.append(player)

volume = Rect(15, 170, 210, 20, fill=0x0, outline=0xFFFFFF)
group.append(volume)

track_time = Rect(15, 210, 210, 20, fill=0x0, outline=0xFFFFFF)
# time = label.Label(font=arial16, x=15, y=215, text='Time', color=0xFFFFFF)
group.append(track_time)

time_inner = Rect(15, 210, 1, 20, fill=0xFFFFFF, outline=0xFFFFFF)
group.append(time_inner)

volume_inner = Rect(15, 170, 1, 20, fill=0xFFFFFF, outline=0xFFFFFF)
group.append(volume_inner)

display.root_group = group
time.sleep(0.01)

width1 = 1

ref_time = time.time()
ela_time = ams.elapsed_time
while radio.connected:
    try:
        if ams.elapsed_time != ela_time:
            ela_time = ams.elapsed_time
            ref_time = time.time()
        title.text = ams.title
        artist.text = ams.artist
        album.text = ams.album
        player.text = ams.player_name
        if ams.volume is not None:
            width = int(16 * 13.125 * float(ams.volume))
            if not width:
                width = 1
            if ams.duration and ams.playing:
                width1 = int(
                    210 * ((time.time() - ref_time + ela_time) / float(ams.duration))
                )
                if not width1:
                    width1 = 1
            elif not ams.duration:
                width1 = 1

            time_inner = Rect(15, 210, width1, 20, fill=0xFFFFFF)  # , outline=0xFFFFFF)
            group[-2] = time_inner
            volume_inner = Rect(
                15, 170, width, 20, fill=0xFFFFFF
            )  # , outline=0xFFFFFF)
            group[-1] = volume_inner

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
            time.sleep(0.35)
            while clue.button_b:
                ams.volume_up()
                time.sleep(0.07)

        # If button A (on the left) is pressed, the volume decreases
        if clue.button_a:
            ams.volume_down()
            time.sleep(0.35)
            while clue.button_a:
                ams.volume_down()
                time.sleep(0.07)
        time.sleep(0.01)
    except (RuntimeError, UnsupportedCommand, AttributeError):
        time.sleep(0.01)
        continue

print("disconnected")
