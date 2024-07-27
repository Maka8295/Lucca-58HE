# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""VC0706 image capture to SD card demo.
You must wire up the VC0706 to the board's serial port, and a SD card holder
to the board's SPI bus.  Use the Feather M0 Adalogger as it includes a SD
card holder pre-wired to the board--this sketch is setup to use the Adalogger!
In addition you MUST also install the following dependent SD card library:
https://github.com/adafruit/Adafruit_CircuitPython_SD
See the guide here for more details on using SD cards with CircuitPython:
https://learn.adafruit.com/micropython-hardware-sd-cards"""

import time

import board
import busio

# import digitalio # Uncomment if your board doesn't support sdcardio
import storage

# import adafruit_sdcard # Uncomment if your board doesn't support sdcardio
import sdcardio  # Comment out if your board doesn't support sdcardio
import adafruit_vc0706


# Configuration:
SD_CS_PIN = board.D10  # CS for SD card (SD_CS is for Feather Adalogger)
IMAGE_FILE = "/sd/image.jpg"  # Full path to file name to save captured image.
# Will overwrite!

# Setup SPI bus (hardware SPI).
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Setup SD card and mount it in the filesystem.
# Uncomment if your board doesn't support sdcardio
# sd_cs = digitalio.DigitalInOut(SD_CS_PIN)
# sdcard = adafruit_sdcard.SDCard(spi, sd_cs)
sdcard = sdcardio.SDCard(
    spi, SD_CS_PIN
)  # Comment out if your board doesn't support sdcardio

vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# Create a serial connection for the VC0706 connection, speed is auto-detected.
uart = busio.UART(board.TX, board.RX)
# Setup VC0706 camera
vc0706 = adafruit_vc0706.VC0706(uart)

# Print the version string from the camera.
print("VC0706 version:")
print(vc0706.version)

# Set the baud rate to 115200 for fastest transfer (its the max speed)
vc0706.baudrate = 115200

# Set the image size.
vc0706.image_size = adafruit_vc0706.IMAGE_SIZE_640x480  # Or set IMAGE_SIZE_320x240 or
# IMAGE_SIZE_160x120
# Note you can also read the property and compare against those values to
# see the current size:
size = vc0706.image_size
if size == adafruit_vc0706.IMAGE_SIZE_640x480:
    print("Using 640x480 size image.")
elif size == adafruit_vc0706.IMAGE_SIZE_320x240:
    print("Using 320x240 size image.")
elif size == adafruit_vc0706.IMAGE_SIZE_160x120:
    print("Using 160x120 size image.")

# Take a picture.
print("Taking a picture in 3 seconds...")
time.sleep(3)
print("SNAP!")
if not vc0706.take_picture():
    raise RuntimeError("Failed to take picture!")

# Print size of picture in bytes.
frame_length = vc0706.frame_length
print("Picture size (bytes): {}".format(frame_length))

# Open a file for writing (overwriting it if necessary).
# This will write 50 bytes at a time using a small buffer.
# You MUST keep the buffer size under 100!
print("Writing image: {}".format(IMAGE_FILE), end="")
stamp = time.monotonic()
# pylint: disable=invalid-name
with open(IMAGE_FILE, "wb") as outfile:
    wcount = 0
    while frame_length > 0:
        # Compute how much data is left to read as the lesser of remaining bytes
        # or the copy buffer size (32 bytes at a time).  Buffer size MUST be
        # a multiple of 4 and under 100.  Stick with 32!
        to_read = min(frame_length, 32)
        copy_buffer = bytearray(to_read)
        # Read picture data into the copy buffer.
        if vc0706.read_picture_into(copy_buffer) == 0:
            raise RuntimeError("Failed to read picture frame data!")
        # Write the data to SD card file and decrement remaining bytes.
        outfile.write(copy_buffer)
        frame_length -= 32
        # Print a dot every 2k bytes to show progress.
        wcount += 1
        if wcount >= 64:
            print(".", end="")
            wcount = 0
# pylint: enable=invalid-name
print()
print("Finished in %0.1f seconds!" % (time.monotonic() - stamp))
# Turn the camera back into video mode.
vc0706.resume_video()
