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

TEXT_URL = "http://wifitest.adafruit.com/testwifi/index.html"
JSON_GET_URL = "http://httpbin.org/get"
JSON_POST_URL = "http://httpbin.org/post"

print("Fetching text from %s" % TEXT_URL)
with requests.get(TEXT_URL) as response:
    print("-" * 40)
    print("Text Response: ", response.text)
    print("-" * 40)

print("Fetching JSON data from %s" % JSON_GET_URL)
with requests.get(JSON_GET_URL) as response:
    print("-" * 40)
    print("JSON Response: ", response.json())
    print("-" * 40)

data = "31F"
print("POSTing data to {0}: {1}".format(JSON_POST_URL, data))
with requests.post(JSON_POST_URL, data=data) as response:
    print("-" * 40)
    json_resp = response.json()
    # Parse out the 'data' key from json_resp dict.
    print("Data received from server:", json_resp["data"])
    print("-" * 40)

json_data = {"Date": "July 25, 2019"}
print("POSTing data to {0}: {1}".format(JSON_POST_URL, json_data))
with requests.post(JSON_POST_URL, json=json_data) as response:
    print("-" * 40)
    json_resp = response.json()
    # Parse out the 'json' key from json_resp dict.
    print("JSON Data received from server:", json_resp["json"])
    print("-" * 40)
