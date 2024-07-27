# SPDX-FileCopyrightText: 2024 DJDevon3
# SPDX-License-Identifier: MIT
# Coded for Circuit Python 8.2.x
"""Mastodon API Example"""

import os
import time

import adafruit_connection_manager
import wifi

import adafruit_requests

# Mastodon V1 API - Public access (no dev creds or app required)
# Visit https://docs.joinmastodon.org/client/public/ for API docs
# For finding your Mastodon numerical UserID
# Example: https://mastodon.YOURSERVER/api/v1/accounts/lookup?acct=YourUserName

MASTODON_SERVER = "mastodon.social"  # Set server instance
MASTODON_USERID = "000000000000000000"  # Numerical UserID you want endpoints from
# Test in browser first, this will pull up a JSON webpage
# https://mastodon.YOURSERVER/api/v1/accounts/YOURUSERIDHERE/statuses?limit=1

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


# Publicly available data no header required
MAST_SOURCE = (
    "https://"
    + MASTODON_SERVER
    + "/api/v1/accounts/"
    + MASTODON_USERID
    + "/statuses?limit=1"
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
        # Print Request to Serial
        print(" | Attempting to GET MASTODON JSON!")

        # Set debug to True for full JSON response.
        # WARNING: may include visible credentials
        # MICROCONTROLLER WARNING: might crash by returning too much data
        DEBUG_RESPONSE = False

        try:
            with requests.get(url=MAST_SOURCE) as mastodon_response:
                mastodon_json = mastodon_response.json()
        except ConnectionError as e:
            print(f"Connection Error: {e}")
            print("Retrying in 10 seconds")
        mastodon_json = mastodon_json[0]
        print(" | ✅ Mastodon JSON!")

        if DEBUG_RESPONSE:
            print(" |  | Full API GET URL: ", MAST_SOURCE)
            mastodon_userid = mastodon_json["account"]["id"]
            print(f" |  | User ID: {mastodon_userid}")
            print(mastodon_json)

        mastodon_name = mastodon_json["account"]["display_name"]
        print(f" |  | Name: {mastodon_name}")
        mastodon_join_date = mastodon_json["account"]["created_at"]
        print(f" |  | Member Since: {mastodon_join_date}")
        mastodon_follower_count = mastodon_json["account"]["followers_count"]
        print(f" |  | Followers: {mastodon_follower_count}")
        mastodon_following_count = mastodon_json["account"]["following_count"]
        print(f" |  | Following: {mastodon_following_count}")
        mastodon_toot_count = mastodon_json["account"]["statuses_count"]
        print(f" |  | Toots: {mastodon_toot_count}")
        mastodon_last_toot = mastodon_json["account"]["last_status_at"]
        print(f" |  | Last Toot: {mastodon_last_toot}")
        mastodon_bio = mastodon_json["account"]["note"]
        print(f" |  | Bio: {mastodon_bio[3:-4]}")  # removes included html "<p> & </p>"

        print("\nFinished!")
        print(f"Board Uptime: {time.monotonic()}")
        print(f"Next Update: {time_calc(SLEEP_TIME)}")
        print("===============================")

    except (ValueError, RuntimeError) as e:
        print(f"Failed to get data, retrying\n {e}")
        time.sleep(60)
        break
    time.sleep(SLEEP_TIME)
