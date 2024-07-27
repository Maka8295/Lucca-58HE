# SPDX-FileCopyrightText: 2017 Tim Cocks for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import board
import busio
import adafruit_vc0706

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
vc0706.image_size = adafruit_vc0706.IMAGE_SIZE_160x120  # Or set IMAGE_SIZE_320x240 or

# Note you can also read the property and compare against those values to
# see the current size:
size = vc0706.image_size
if size == adafruit_vc0706.IMAGE_SIZE_640x480:
    print("Using 640x480 size image.")
elif size == adafruit_vc0706.IMAGE_SIZE_320x240:
    print("Using 320x240 size image.")
elif size == adafruit_vc0706.IMAGE_SIZE_160x120:
    print("Using 160x120 size image.")

# Turn on motion detection
vc0706.motion_detection = True

# Detect motion
while True:
    if vc0706.motion_detected:
        print("Motion detected!")
    else:
        print("....")
