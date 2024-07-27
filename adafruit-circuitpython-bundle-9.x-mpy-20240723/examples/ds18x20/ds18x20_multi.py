# SPDX-FileCopyrightText: 2020 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Example of specifying multiple sensors using explicit ROM codes.
# These ROM codes need to be determined ahead of time. Use `ow_bus.scan()`.
#
# (1) Connect one sensor at a time
# (2) Use `ow_bus.scan()[0].rom` to determine ROM code
# (3) Use ROM code to specify sensors (see this example)

import time
import board
from adafruit_onewire.bus import OneWireBus, OneWireAddress
from adafruit_ds18x20 import DS18X20

# !!!! REPLACE THESE WITH ROM CODES FOR YOUR SENSORS !!!!
ROM1 = b"(\xbb\xfcv\x08\x00\x00\xe2"
ROM2 = b"(\xb3t\xd3\x08\x00\x00\x9e"
ROM3 = b"(8`\xd4\x08\x00\x00i"
# !!!! REPLACE THESE WITH ROM CODES FOR YOUR SENSORS !!!!

# Initialize one-wire bus on board pin D5.
ow_bus = OneWireBus(board.D5)

# Uncomment this to get a listing of currently attached ROMs
# for device in ow_bus.scan():
#     print(device.rom)

# Use pre-determined ROM codes for each sensors
temp1 = DS18X20(ow_bus, OneWireAddress(ROM1))
temp2 = DS18X20(ow_bus, OneWireAddress(ROM2))
temp3 = DS18X20(ow_bus, OneWireAddress(ROM3))

# Main loop to print the temperatures every second.
while True:
    print("Temperature 1 = {}".format(temp1.temperature))
    print("Temperature 2 = {}".format(temp2.temperature))
    print("Temperature 3 = {}".format(temp3.temperature))
    print("-" * 20)
    time.sleep(1)
