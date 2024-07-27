# SPDX-FileCopyrightText: 2022 Alec Delaney
# SPDX-License-Identifier: MIT
# Coded for Circuit Python 9.0
""" Multiple Cookies Example written for MagTag """

import os

import adafruit_connection_manager
import wifi

import adafruit_requests

# Get WiFi details, ensure these are setup in settings.toml
ssid = os.getenv("CIRCUITPY_WIFI_SSID")
password = os.getenv("CIRCUITPY_WIFI_PASSWORD")

COOKIE_TEST_URL = "https://www.adafruit.com"

# Initalize Wifi, Socket Pool, Request Session
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)

print(f"\nConnecting to {ssid}...")
try:
    # Connect to the Wi-Fi network
    wifi.radio.connect(ssid, password)
except OSError as e:
    print(f"❌ OSError: {e}")
print("✅ Wifi!")

# URL GET Request
with requests.get(COOKIE_TEST_URL) as response:
    print(f" | Fetching Cookies: {COOKIE_TEST_URL}")

    # Spilt up the cookies by ", "
    elements = response.headers["set-cookie"].split(", ")

    # NOTE: Some cookies use ", " when describing dates.  This code will iterate through
    # the previously split up 'set-cookie' header value and piece back together cookies
    # that were accidentally split up for this reason
    days_of_week = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")
    elements_iter = iter(elements)
    cookie_list = []
    for element in elements_iter:
        captured_day = [day for day in days_of_week if element.endswith(day)]
        if captured_day:
            cookie_list.append(element + ", " + next(elements_iter))
        else:
            cookie_list.append(element)

    # Pring the information about the cookies
    print(f" | Total Cookies: {len(cookie_list)}")
    print("-" * 80)

    for cookie in cookie_list:
        print(f" | 🍪 {cookie}")
        print("-" * 80)

print("Finished!")
