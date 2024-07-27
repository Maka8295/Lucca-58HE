# SPDX-FileCopyrightText: 2024 Justin Myers for Adafruit Industries
# SPDX-FileCopyrightText: 2024 anecdata for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""Print out time based on NTP, using connection manager"""

import adafruit_connection_manager
import adafruit_ntp

# determine which radio is available
try:
    import wifi
    import os

    # adjust method to get credentials as necessary...
    wifi_ssid = os.getenv("CIRCUITPY_WIFI_SSID")
    wifi_password = os.getenv("CIRCUITPY_WIFI_PASSWORD")
    radio = wifi.radio
    while not radio.connected:
        radio.connect(wifi_ssid, wifi_password)
except ImportError:
    import board
    from digitalio import DigitalInOut
    from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K

    # adjust with busio.SPI() as necessary...
    spi = board.SPI()
    # adjust pin for the specific board...
    eth_cs = DigitalInOut(board.D10)
    radio = WIZNET5K(spi, eth_cs)

# get the socket pool from connection manager
socket = adafruit_connection_manager.get_radio_socketpool(radio)

# adjust tz_offset for locale, only ping NTP server every hour
ntp = adafruit_ntp.NTP(socket, tz_offset=-5, cache_seconds=3600)

print(ntp.datetime)
