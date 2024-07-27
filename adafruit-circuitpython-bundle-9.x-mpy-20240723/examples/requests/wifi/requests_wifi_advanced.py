# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
# Updated for Circuit Python 9.0

""" WiFi Advanced Example """

import os

import adafruit_connection_manager
import wifi

import adafruit_requests

# Get WiFi details, ensure these are setup in settings.toml
ssid = os.getenv("CIRCUITPY_WIFI_SSID")
password = os.getenv("CIRCUITPY_WIFI_PASSWORD")

# Initalize Wifi, Socket Pool, Request Session
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)
rssi = wifi.radio.ap_info.rssi

# URL for GET request
JSON_GET_URL = "https://httpbin.org/get"
# Define a custom header as a dict.
headers = {"user-agent": "blinka/1.0.0"}

print(f"\nConnecting to {ssid}...")
print(f"Signal Strength: {rssi}")
try:
    # Connect to the Wi-Fi network
    wifi.radio.connect(ssid, password)
except OSError as e:
    print(f"❌ OSError: {e}")
print("✅ Wifi!")

# Define a custom header as a dict.
headers = {"user-agent": "blinka/1.0.0"}
print(f" | Fetching URL {JSON_GET_URL}")

# Use with statement for retreiving GET request data
with requests.get(JSON_GET_URL, headers=headers) as response:
    json_data = response.json()
    headers = json_data["headers"]
    content_type = response.headers.get("content-type", "")
    date = response.headers.get("date", "")
    if response.status_code == 200:
        print(f" | 🆗 Status Code: {response.status_code}")
    else:
        print(f" | ❌ Status Code: {response.status_code}")
    print(f" |  | Custom User-Agent Header: {headers['User-Agent']}")
    print(f" |  | Content-Type: {content_type}")
    print(f" |  | Response Timestamp: {date}")
