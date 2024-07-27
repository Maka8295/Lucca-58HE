# SPDX-FileCopyrightText: 2022 Scott Shawcroft for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Example demonstrating how to set the realtime clock (RTC) based on NTP time."""

import time

import rtc
import socketpool
import wifi

import adafruit_ntp

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

wifi.radio.connect(secrets["ssid"], secrets["password"])

pool = socketpool.SocketPool(wifi.radio)
ntp = adafruit_ntp.NTP(pool, tz_offset=0, cache_seconds=3600)

# NOTE: This changes the system time so make sure you aren't assuming that time
# doesn't jump.
rtc.RTC().datetime = ntp.datetime

while True:
    print(time.localtime())
    time.sleep(1)
