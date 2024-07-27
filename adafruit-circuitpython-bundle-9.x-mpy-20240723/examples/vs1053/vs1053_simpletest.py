# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Example of sound playback from VS1053 FeatherWing.  Can be modified to work
# with the breakout by changing the SD card and SPI pins mentioned below.
# NOTE:
# Unfortunately this doesn't work--the loop isn't fast enough to feed the VS1053
# data at the rate it needs for playback.  You'll see very erratic behavior with
# the VS1053 making static, stopping, and eventually requiring a hard reset.
# We'll need to look into interrupt support perhaps to monitor DREQ like in the
# arduino library.  Basic sine wave playback does however work and monitoring
# of attributes like status register and other VS1053 state is accessible.
import board
import busio
import digitalio
import storage

import adafruit_sdcard
import adafruit_vs1053


# Define pins connected to VS1053:

# For FeatherWing with Feather M0:
SDCS = board.D5  # Pin connected to SD card CS line.
MP3CS = board.D6  # Pin connected to VS1053 CS line.
DREQ = board.D9  # Pin connected to VS1053 DREQ line.
XDCS = board.D10  # Pin connected to VS1053 D/C line.


# Other configuration:
PLAYBACK_FILE = "/sd/test.wav"  # Name of file to play.
# This should be the full path
# including /sd prefix if on
# sd card.

BUFFER_SIZE = 128  # Size in bytes of the MP3 data buffer for sending data to
# the VS1053.


# Setup SPI bus (hardware SPI).
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Setup SD card and mount it in the filesystem.
sd_cs = digitalio.DigitalInOut(SDCS)
sdcard = adafruit_sdcard.SDCard(spi, sd_cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# To list all the files on the SD card root uncomment:
# import os
# print('SD card root contains:')
# print(os.listdir('/sd'))

# Setup VS1053.
vs1053 = adafruit_vs1053.VS1053(spi, MP3CS, XDCS, DREQ)

# Set volume of left and right channels.
# Value ranges from 0 to 255 for each channel, the lower the higher volume.
vs1053.set_volume(0, 0)

# Play a test tone (this works).
print("Playing test tone for two seconds...")
vs1053.sine_test(0x44, 2.0)
print("Done playing tone!")

# Play back a MP3 file by starting playback, then reading a buffer of data
# at a time and sending it to the VS1053.
# Unfortunately this doesn't work--the loop isn't fast enough to feed the VS1053
# data at the rate it needs for playback.  You'll see very erratic behavior with
# the VS1053 making static, stopping, and eventually requiring a hard reset.
# We'll need to look into interrupt support perhaps to monitor DREQ like in the
# arduino library.
print("Playing {}...".format(PLAYBACK_FILE))
vs1053.start_playback()
with open(PLAYBACK_FILE, "rb") as infile:
    music_data = infile.read(BUFFER_SIZE)
    while music_data is not None and music_data != "":
        while not vs1053.ready_for_data:
            pass
        vs1053.play_data(music_data, end=len(music_data))
        music_data = infile.read(BUFFER_SIZE)

print("Done!")
