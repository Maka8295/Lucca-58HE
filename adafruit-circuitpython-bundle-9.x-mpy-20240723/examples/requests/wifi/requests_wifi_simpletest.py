# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
# Updated for Circuit Python 9.0
""" WiFi Simpletest """

import os

import adafruit_connection_manager
import wifi

import adafruit_requests

# Get WiFi details, ensure these are setup in settings.toml
ssid = os.getenv("CIRCUITPY_WIFI_SSID")
password = os.getenv("CIRCUITPY_WIFI_PASSWORD")

TEXT_URL = "http://wifitest.adafruit.com/testwifi/index.html"
JSON_GET_URL = "https://httpbin.org/get"
JSON_POST_URL = "https://httpbin.org/post"

# Initalize Wifi, Socket Pool, Request Session
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)
rssi = wifi.radio.ap_info.rssi

print(f"\nConnecting to {ssid}...")
print(f"Signal Strength: {rssi}")
try:
    # Connect to the Wi-Fi network
    wifi.radio.connect(ssid, password)
except OSError as e:
    print(f"❌ OSError: {e}")
print("✅ Wifi!")

print(f" | GET Text Test: {TEXT_URL}")
with requests.get(TEXT_URL) as response:
    print(f" | ✅ GET Response: {response.text}")
print("-" * 80)

print(f" | GET Full Response Test: {JSON_GET_URL}")
with requests.get(JSON_GET_URL) as response:
    print(f" | ✅ Unparsed Full JSON Response: {response.json()}")
print("-" * 80)

DATA = "This is an example of a JSON value"
print(f" | ✅ JSON 'value' POST Test: {JSON_POST_URL} {DATA}")
with requests.post(JSON_POST_URL, data=DATA) as response:
    json_resp = response.json()
    # Parse out the 'data' key from json_resp dict.
    print(f" | ✅ JSON 'value' Response: {json_resp['data']}")
print("-" * 80)

json_data = {"Date": "January 1, 1970"}
print(f" | ✅ JSON 'key':'value' POST Test: {JSON_POST_URL} {json_data}")
with requests.post(JSON_POST_URL, json=json_data) as response:
    json_resp = response.json()
    # Parse out the 'json' key from json_resp dict.
    print(f" | ✅ JSON 'key':'value' Response: {json_resp['json']}")
print("-" * 80)

print("Finished!")
