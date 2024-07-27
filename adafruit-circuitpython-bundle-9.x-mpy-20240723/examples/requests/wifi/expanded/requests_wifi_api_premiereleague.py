# SPDX-FileCopyrightText: 2024 DJDevon3
# SPDX-License-Identifier: MIT
# Coded for Circuit Python 8.2.x
"""Premiere League Total Players API Example"""

import os
import time

import adafruit_connection_manager
import adafruit_json_stream as json_stream
import wifi

import adafruit_requests

# Public API. No user or token required

# Get WiFi details, ensure these are setup in settings.toml
ssid = os.getenv("CIRCUITPY_WIFI_SSID")
password = os.getenv("CIRCUITPY_WIFI_PASSWORD")

# API Polling Rate
# 900 = 15 mins, 1800 = 30 mins, 3600 = 1 hour
SLEEP_TIME = 900

# Initalize Wifi, Socket Pool, Request Session
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)

# Publicly available data no header required
PREMIERE_LEAGUE_SOURCE = "https://fantasy.premierleague.com/api/bootstrap-static/"


def time_calc(input_time):
    """Converts seconds to minutes/hours/days"""
    if input_time < 60:
        return f"{input_time:.0f} seconds"
    if input_time < 3600:
        return f"{input_time / 60:.0f} minutes"
    if input_time < 86400:
        return f"{input_time / 60 / 60:.0f} hours"
    return f"{input_time / 60 / 60 / 24:.1f} days"


while True:
    # Connect to Wi-Fi
    print("\nConnecting to WiFi...")
    while not wifi.radio.ipv4_address:
        try:
            wifi.radio.connect(ssid, password)
        except ConnectionError as e:
            print("❌ Connection Error:", e)
            print("Retrying in 10 seconds")
    print("✅ Wifi!")

    try:
        print(" | Attempting to GET Premiere League JSON!")

        # Set debug to True for full JSON response.
        # WARNING: may include visible credentials
        # MICROCONTROLLER WARNING: might crash by returning too much data
        DEBUG_RESPONSE = False

        try:
            with requests.get(url=PREMIERE_LEAGUE_SOURCE) as PREMIERE_LEAGUE_RESPONSE:
                pl_json = json_stream.load(PREMIERE_LEAGUE_RESPONSE.iter_content(32))
        except ConnectionError as e:
            print(f"Connection Error: {e}")
            print("Retrying in 10 seconds")
        print(" | ✅ Premiere League JSON!")

        print(f" | Total Premiere League Players: {pl_json['total_players']}")

        print("\nFinished!")
        print(f"Board Uptime: {time.monotonic()}")
        print(f"Next Update: {time_calc(SLEEP_TIME)}")
        print("===============================")

    except (ValueError, RuntimeError) as e:
        print(f"Failed to get data, retrying\n {e}")
        time.sleep(60)
        break
    time.sleep(SLEEP_TIME)
