# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
from adafruit_onewire.bus import OneWireBus

# Create the 1-Wire Bus
# Use whatever pin you've connected to on your board
ow_bus = OneWireBus(board.D2)

# Reset and check for presence pulse.
# This is basically - "is there anything out there?"
print("Resetting bus...", end="")
if ow_bus.reset():
    print("OK.")
else:
    raise RuntimeError("Nothing found on bus.")

# Run a scan to get all of the device ROM values
print("Scanning for devices...", end="")
devices = ow_bus.scan()
print("OK.")
print("Found {} device(s).".format(len(devices)))

# For each device found, print out some info
for i, d in enumerate(devices):
    print("Device {:>3}".format(i))
    print("\tSerial Number = ", end="")
    for byte in d.serial_number:
        print("0x{:02x} ".format(byte), end="")
    print("\n\tFamily = 0x{:02x}".format(d.family_code))

# Usage beyond this is device specific. See a CircuitPython library for a 1-Wire
# device for examples and how OneWireDevice is used.
