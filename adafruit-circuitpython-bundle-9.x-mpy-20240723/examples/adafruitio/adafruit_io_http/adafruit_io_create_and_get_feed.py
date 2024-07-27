# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
Example using create_and_get_feed. Creates a new feed if it does not exist and sends to it, or
sends to an existing feed once it has been created.
"""
import ssl
import adafruit_requests
import socketpool
import wifi
import microcontroller
from adafruit_io.adafruit_io import IO_HTTP

# Add a secrets.py to your filesystem that has a dictionary called secrets with "ssid" and
# "password" keys with your WiFi credentials, and "aio_username" and "aio_key" keys with your
# Adafruit IO credentials, DO NOT share that file or commit it into Git or other
# source control.
# pylint: disable=no-name-in-module,wrong-import-order
try:
    from secrets import secrets
except ImportError:
    print(
        "WiFi and Adafruit IO credentials are kept in secrets.py, please add them there!"
    )
    raise

# Connect to Wi-Fi using credentials from secrets.py
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Connected to {}!".format(secrets["ssid"]))
print("IP:", wifi.radio.ipv4_address)

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

# Obtain Adafruit IO credentials from secrets.py
aio_username = secrets["aio_username"]
aio_key = secrets["aio_key"]

# Initialize an Adafruit IO HTTP API object
io = IO_HTTP(aio_username, aio_key, requests)

# Create temperature variable using the CPU temperature and print the current value.
temperature = microcontroller.cpu.temperature
print("Current CPU temperature: {0} C".format(temperature))

# Create and get feed.
io.send_data(io.create_and_get_feed("cpu-temperature-feed")["key"], temperature)
