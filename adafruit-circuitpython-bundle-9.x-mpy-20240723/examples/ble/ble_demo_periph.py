# SPDX-FileCopyrightText: 2020 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Used with ble_demo_central.py. Receives Bluefruit LE ColorPackets from a central,
and updates a Circuit Playground to show the history of the received packets.
"""

import board
import neopixel

# Only the packet classes that are imported will be known to Packet.
from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.color_packet import ColorPacket

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

NUM_PIXELS = 10
np = neopixel.NeoPixel(board.NEOPIXEL, NUM_PIXELS, brightness=0.1)
next_pixel = 0


def mod(i):
    """Wrap i to modulus NUM_PIXELS."""
    return i % NUM_PIXELS


ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

while True:
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass
    while ble.connected:
        packet = Packet.from_stream(uart)
        if isinstance(packet, ColorPacket):
            print(packet.color)
            np[next_pixel] = packet.color
            np[mod(next_pixel + 1)] = (0, 0, 0)
        next_pixel = (next_pixel + 1) % NUM_PIXELS
