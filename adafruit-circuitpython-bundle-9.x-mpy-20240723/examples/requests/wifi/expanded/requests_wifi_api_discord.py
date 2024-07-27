# SPDX-FileCopyrightText: 2024 DJDevon3
# SPDX-License-Identifier: MIT
# Coded for Circuit Python 8.2.x
"""Discord Web Scrape Example"""

import os
import time

import adafruit_connection_manager
import wifi

import adafruit_requests

# Active Logged in User Account Required
# WEB SCRAPE authorization key required. Visit URL below.
# Learn how: https://github.com/lorenz234/Discord-Data-Scraping

# Ensure this is in settings.toml
# DISCORD_AUTHORIZATION = "Approximately 70 Character Hash Here"

# Get WiFi details, ensure these are setup in settings.toml
ssid = os.getenv("CIRCUITPY_WIFI_SSID")
password = os.getenv("CIRCUITPY_WIFI_PASSWORD")
discord_auth = os.getenv("DISCORD_AUTHORIZATION")

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


DISCORD_HEADER = {"Authorization": "" + discord_auth}
DISCORD_SOURCE = (
    "https://discord.com/api/v10/guilds/"
    + "327254708534116352"  # Adafruit Discord ID
    + "/preview"
)

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
        print(" | Attempting to GET Discord JSON!")
        # Set debug to True for full JSON response.
        # WARNING: may include visible credentials
        # MICROCONTROLLER WARNING: might crash by returning too much data
        DEBUG_RESPONSE = False

        try:
            with requests.get(
                url=DISCORD_SOURCE, headers=DISCORD_HEADER
            ) as discord_response:
                discord_json = discord_response.json()
        except ConnectionError as e:
            print(f"Connection Error: {e}")
            print("Retrying in 10 seconds")
        print(" | ✅ Discord JSON!")

        if DEBUG_RESPONSE:
            print(f" |  | Full API GET URL: {DISCORD_SOURCE}")
            print(f" |  | JSON Dump: {discord_json}")

        discord_name = discord_json["name"]
        print(f" |  | Name: {discord_name}")

        discord_description = discord_json["description"]
        print(f" |  | Description: {discord_description}")

        discord_all_members = discord_json["approximate_member_count"]
        print(f" |  | Members: {discord_all_members}")

        discord_all_members_online = discord_json["approximate_presence_count"]
        print(f" |  | Online: {discord_all_members_online}")

        print("\nFinished!")
        print(f"Board Uptime: {time.monotonic()}")
        print(f"Next Update: {time_calc(SLEEP_TIME)}")
        print("===============================")

    except (ValueError, RuntimeError) as e:
        print(f"Failed to get data, retrying\n {e}")
        time.sleep(60)
        break
    time.sleep(SLEEP_TIME)
