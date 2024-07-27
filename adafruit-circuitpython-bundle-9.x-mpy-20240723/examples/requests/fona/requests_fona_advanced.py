# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import os
import time

import adafruit_connection_manager
import adafruit_fona.adafruit_fona_network as network
import adafruit_fona.adafruit_fona_socket as pool
import board
import busio
import digitalio
from adafruit_fona.adafruit_fona import FONA  # pylint: disable=unused-import
from adafruit_fona.fona_3g import FONA3G  # pylint: disable=unused-import

import adafruit_requests

# Get GPRS details, ensure these are setup in settings.toml
apn = os.getenv("APN")
apn_username = os.getenv("APN_USERNAME")
apn_password = os.getenv("APN_PASSWORD")

# Create a serial connection for the FONA connection
uart = busio.UART(board.TX, board.RX)
rst = digitalio.DigitalInOut(board.D4)

# Use this for FONA800 and FONA808
radio = FONA(uart, rst)

# Use this for FONA3G
# radio = FONA3G(uart, rst)

# Initialize cellular data network
network = network.CELLULAR(radio, (apn, apn_username, apn_password))

while not network.is_attached:
    print("Attaching to network...")
    time.sleep(0.5)
print("Attached!")

while not network.is_connected:
    print("Connecting to network...")
    network.connect()
    time.sleep(0.5)
print("Network Connected!")

# Initialize a requests session
ssl_context = adafruit_connection_manager.create_fake_ssl_context(pool, radio)
requests = adafruit_requests.Session(pool, ssl_context)

JSON_GET_URL = "http://httpbin.org/get"

# Define a custom header as a dict.
headers = {"user-agent": "blinka/1.0.0"}

print("Fetching JSON data from %s..." % JSON_GET_URL)
with requests.get(JSON_GET_URL, headers=headers) as response:
    print("-" * 60)

    json_data = response.json()
    headers = json_data["headers"]
    print("Response's Custom User-Agent Header: {0}".format(headers["User-Agent"]))
    print("-" * 60)

    # Read Response's HTTP status code
    print("Response HTTP Status Code: ", response.status_code)
    print("-" * 60)
