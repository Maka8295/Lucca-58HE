# SPDX-FileCopyrightText: 2024 DJDevon3
# SPDX-License-Identifier: MIT
# Coded for Circuit Python 8.2.x
"""Discord Active Online Shields.IO Example"""

import os
import time

import adafruit_connection_manager
import wifi

import adafruit_requests

# Public API. No user or token required
# JSON web scrape from SHIELDS.IO
# Adafruit uses Shields.IO to see online users

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


def time_calc(input_time):
    """Converts seconds to minutes/hours/days"""
    if input_time < 60:
        return f"{input_time:.0f} seconds"
    if input_time < 3600:
        return f"{input_time / 60:.0f} minutes"
    if input_time < 86400:
        return f"{input_time / 60 / 60:.0f} hours"
    return f"{input_time / 60 / 60 / 24:.1f} days"


# Originally attempted to use SVG. Found JSON exists with same filename.
# https://img.shields.io/discord/327254708534116352.svg
ADA_DISCORD_JSON = "https://img.shields.io/discord/327254708534116352.json"

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
        print(" | Attempting to GET Adafruit Discord JSON!")
        # Set debug to True for full JSON response.
        DEBUG_RESPONSE = True

        try:
            with requests.get(url=ADA_DISCORD_JSON) as shieldsio_response:
                shieldsio_json = shieldsio_response.json()
        except ConnectionError as e:
            print(f"Connection Error: {e}")
            print("Retrying in 10 seconds")
        print(" | ✅ Adafruit Discord JSON!")

        if DEBUG_RESPONSE:
            print(" |  | Full API GET URL: ", ADA_DISCORD_JSON)
            print(" |  | JSON Dump: ", shieldsio_json)

        ada_users = shieldsio_json["value"]
        ONLINE_STRING = " online"
        REPLACE_WITH_NOTHING = ""
        active_users = ada_users.replace(ONLINE_STRING, REPLACE_WITH_NOTHING)
        print(f" |  | Active Online Users: {active_users}")

        print("\nFinished!")
        print(f"Board Uptime: {time.monotonic()}")
        print(f"Next Update: {time_calc(SLEEP_TIME)}")
        print("===============================")

    except (ValueError, RuntimeError) as e:
        print(f"Failed to get data, retrying\n {e}")
        time.sleep(60)
        break
    time.sleep(SLEEP_TIME)
