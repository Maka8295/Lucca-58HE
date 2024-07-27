# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This demo connects to a magic light and has it do a colorwheel."""
from rainbowio import colorwheel
import adafruit_ble
import _bleio

from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble_magic_light import MagicLightService

# CircuitPython <6 uses its own ConnectionError type. So, is it if available. Otherwise,
# the built in ConnectionError is used.
connection_error = ConnectionError
if hasattr(_bleio, "ConnectionError"):
    connection_error = _bleio.ConnectionError


def find_connection():
    for connection in radio.connections:
        if MagicLightService not in connection:
            continue
        return connection, connection[MagicLightService]
    return None, None


# Start advertising before messing with the display so that we can connect immediately.
radio = adafruit_ble.BLERadio()

active_connection, pixels = find_connection()
current_notification = None
app_icon_file = None
while True:
    if not active_connection:
        print("Scanning for Magic Light")
        for scan in radio.start_scan(ProvideServicesAdvertisement):
            if MagicLightService in scan.services:
                active_connection = radio.connect(scan)
                try:
                    pixels = active_connection[MagicLightService]
                except connection_error:
                    print("disconnected")
                    continue
                break
        radio.stop_scan()

    i = 0
    while active_connection.connected:
        pixels[0] = colorwheel(i % 256)
        i += 1

    active_connection = None
