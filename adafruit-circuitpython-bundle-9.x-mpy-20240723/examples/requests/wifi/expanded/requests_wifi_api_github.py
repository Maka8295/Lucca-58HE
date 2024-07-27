# SPDX-FileCopyrightText: 2024 DJDevon3
# SPDX-License-Identifier: MIT
# Coded for Circuit Python 9.x
"""Github API Example"""

import os
import time

import adafruit_connection_manager
import wifi

import adafruit_requests

# Github developer token required.
username = os.getenv("GITHUB_USERNAME")
token = os.getenv("GITHUB_TOKEN")

# Get WiFi details, ensure these are setup in settings.toml
ssid = os.getenv("CIRCUITPY_WIFI_SSID")
password = os.getenv("CIRCUITPY_WIFI_PASSWORD")

# API Polling Rate
# 900 = 15 mins, 1800 = 30 mins, 3600 = 1 hour
SLEEP_TIME = 900

# Set debug to True for full JSON response.
# WARNING: may include visible credentials
DEBUG = False

# Initalize Wifi, Socket Pool, Request Session
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)

GITHUB_HEADER = {"Authorization": " token " + token}
GITHUB_SOURCE = "https://api.github.com/users/" + username


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
        print(" | Attempting to GET Github JSON!")
        try:
            with requests.get(
                url=GITHUB_SOURCE, headers=GITHUB_HEADER
            ) as github_response:
                github_json = github_response.json()
        except ConnectionError as e:
            print("Connection Error:", e)
            print("Retrying in 10 seconds")
        print(" | ✅ Github JSON!")

        github_joined = github_json["created_at"]
        print(" |  | Join Date: ", github_joined)

        github_id = github_json["id"]
        print(" |  | UserID: ", github_id)

        github_location = github_json["location"]
        print(" |  | Location: ", github_location)

        github_name = github_json["name"]
        print(" |  | Username: ", github_name)

        github_repos = github_json["public_repos"]
        print(" |  | Respositores: ", github_repos)

        github_followers = github_json["followers"]
        print(" |  | Followers: ", github_followers)
        github_bio = github_json["bio"]
        print(" |  | Bio: ", github_bio)

        if DEBUG:
            print("Full API GET URL: ", GITHUB_SOURCE)
            print(github_json)

        print("\nFinished!")
        print(f"Board Uptime: {time_calc(time.monotonic())}")
        print(f"Next Update: {time_calc(SLEEP_TIME)}")
        print("===============================")

    except (ValueError, RuntimeError) as e:
        print(f"Failed to get data, retrying\n {e}")
        time.sleep(60)
        break
    time.sleep(SLEEP_TIME)
