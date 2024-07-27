# SPDX-FileCopyrightText: 2024 DJDevon3
# SPDX-License-Identifier: MIT
# Coded for Circuit Python 8.2.x
"""Twitch API Example"""

import os
import time

import adafruit_connection_manager
import wifi

import adafruit_requests

# Twitch Developer Account & oauth App Required:
# Visit https://dev.twitch.tv/console to create an app
# Ensure these are in settings.toml
# TWITCH_CLIENT_ID = "Your Developer APP ID Here"
# TWITCH_CLIENT_SECRET = "APP ID secret here"
# TWITCH_USER_ID = "Your Twitch UserID here"

# Get WiFi details, ensure these are setup in settings.toml
ssid = os.getenv("CIRCUITPY_WIFI_SSID")
password = os.getenv("CIRCUITPY_WIFI_PASSWORD")
TWITCH_CID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_CS = os.getenv("TWITCH_CLIENT_SECRET")
# For finding your Twitch User ID
# https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/
TWITCH_UID = os.getenv("TWITCH_USER_ID")

# API Polling Rate
# 900 = 15 mins, 1800 = 30 mins, 3600 = 1 hour
SLEEP_TIME = 900

# Set DEBUG to True for full JSON response.
# STREAMER WARNING: Credentials will be viewable
DEBUG = False

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


def _format_datetime(datetime):
    """F-String formatted struct time conversion"""
    return (
        f"{datetime.tm_mon:02}/"
        + f"{datetime.tm_mday:02}/"
        + f"{datetime.tm_year:02} "
        + f"{datetime.tm_hour:02}:"
        + f"{datetime.tm_min:02}:"
        + f"{datetime.tm_sec:02}"
    )


# First we use Client ID & Client Secret to create a token with POST
# No user interaction is required for this type of scope (implicit grant flow)
twitch_0auth_header = {"Content-Type": "application/x-www-form-urlencoded"}
TWITCH_0AUTH_TOKEN = "https://id.twitch.tv/oauth2/token"

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
        # ------------- POST FOR BEARER TOKEN -----------------
        print(" | Attempting Bearer Token Request!")
        if DEBUG:
            print(f"Full API GET URL: {TWITCH_0AUTH_TOKEN}")
        twitch_0auth_data = (
            "&client_id="
            + TWITCH_CID
            + "&client_secret="
            + TWITCH_CS
            + "&grant_type=client_credentials"
        )

        # POST REQUEST
        try:
            with requests.post(
                url=TWITCH_0AUTH_TOKEN,
                data=twitch_0auth_data,
                headers=twitch_0auth_header,
            ) as twitch_0auth_response:
                twitch_0auth_json = twitch_0auth_response.json()
                twitch_access_token = twitch_0auth_json["access_token"]
        except ConnectionError as e:
            print(f"Connection Error: {e}")
            print("Retrying in 10 seconds")
        print(" | 🔑 Token Authorized!")

        # STREAMER WARNING: your client secret will be viewable
        if DEBUG:
            print(f"JSON Dump: {twitch_0auth_json}")
            print(f"Header: {twitch_0auth_header}")
            print(f"Access Token: {twitch_access_token}")
            twitch_token_type = twitch_0auth_json["token_type"]
            print(f"Token Type: {twitch_token_type}")

        twitch_token_expiration = twitch_0auth_json["expires_in"]
        print(f" | Token Expires in: {time_calc(twitch_token_expiration)}")

        # ----------------------------- GET DATA --------------------
        # Bearer token is refreshed every time script runs :)
        # Twitch sets token expiration to about 64 days
        # Helix is the name of the current Twitch API
        # Now that we have POST bearer token we can do a GET for data
        # -----------------------------------------------------------
        twitch_header = {
            "Authorization": "Bearer " + twitch_access_token + "",
            "Client-Id": "" + TWITCH_CID + "",
        }
        TWITCH_FOLLOWERS_SOURCE = (
            "https://api.twitch.tv/helix/channels"
            + "/followers?"
            + "broadcaster_id="
            + TWITCH_UID
        )
        print(" | Attempting to GET Twitch JSON!")
        try:
            with requests.get(
                url=TWITCH_FOLLOWERS_SOURCE, headers=twitch_header
            ) as twitch_response:
                twitch_json = twitch_response.json()
        except ConnectionError as e:
            print(f"Connection Error: {e}")
            print("Retrying in 10 seconds")

        if DEBUG:
            print(f" | Full API GET URL: {TWITCH_FOLLOWERS_SOURCE}")
            print(f" | Header: {twitch_header}")
            print(f" | JSON Full Response: {twitch_json}")

        if "status" in twitch_json:
            twitch_error_status = twitch_json["status"]
            print(f"❌ Status: {twitch_error_status}")

        if "error" in twitch_json:
            twitch_error = twitch_json["error"]
            print(f"❌ Error: {twitch_error}")

        if "message" in twitch_json:
            twitch_error_msg = twitch_json["message"]
            print(f"❌ Message: {twitch_error_msg}")

        if "total" in twitch_json:
            print(" | ✅ Twitch JSON!")
            twitch_followers = twitch_json["total"]
            print(f" |  | Followers: {twitch_followers}")

        print("\nFinished!")
        print(f"Board Uptime: {time_calc(time.monotonic())}")
        print(f"Next Update: {time_calc(SLEEP_TIME)}")
        print("===============================")

    except (ValueError, RuntimeError) as e:
        print(f"Failed to get data, retrying\n {e}")
        time.sleep(60)
        break
    time.sleep(SLEEP_TIME)
