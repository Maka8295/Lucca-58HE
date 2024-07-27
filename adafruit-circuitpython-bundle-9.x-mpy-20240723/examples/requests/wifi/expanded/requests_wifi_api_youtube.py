# SPDX-FileCopyrightText: 2024 DJDevon3
# SPDX-License-Identifier: MIT
# Coded for Circuit Python 8.2.x
"""YouTube API Subscriber Count Example"""

import os
import time

import adafruit_connection_manager
import wifi

import adafruit_requests

# Initalize Wifi, Socket Pool, Request Session
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)

# API Polling Rate
# 900 = 15 mins, 1800 = 30 mins, 3600 = 1 hour
SLEEP_TIME = 900

# Set debug to True for full JSON response.
# WARNING: Will show credentials
DEBUG = False

# Ensure these are uncommented and in settings.toml
# YOUTUBE_USERNAME = "Your YouTube Username",
# YOUTUBE_TOKEN = "Your long API developer token",

# Get WiFi details, ensure these are setup in settings.toml
ssid = os.getenv("CIRCUITPY_WIFI_SSID")
password = os.getenv("CIRCUITPY_WIFI_PASSWORD")
# Requires YouTube/Google API key
# https://console.cloud.google.com/apis/dashboard
YT_USERNAME = os.getenv("YOUTUBE_USERNAME")
YT_TOKEN = os.getenv("YOUTUBE_TOKEN")


def time_calc(input_time):
    """Converts seconds to minutes/hours/days"""
    if input_time < 60:
        return f"{input_time:.0f} seconds"
    if input_time < 3600:
        return f"{input_time / 60:.0f} minutes"
    if input_time < 86400:
        return f"{input_time / 60 / 60:.0f} hours"
    return f"{input_time / 60 / 60 / 24:.1f} days"


# https://youtube.googleapis.com/youtube/v3/channels?part=statistics&forUsername=[YOUR_USERNAME]&key=[YOUR_API_KEY]
YOUTUBE_SOURCE = (
    "https://youtube.googleapis.com/youtube/v3/channels?part=statistics&forUsername="
    + str(YT_USERNAME)
    + "&key="
    + str(YT_TOKEN)
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
        print(" | Attempting to GET YouTube JSON...")
        try:
            with requests.get(url=YOUTUBE_SOURCE) as youtube_response:
                youtube_json = youtube_response.json()
        except ConnectionError as e:
            print("Connection Error:", e)
            print("Retrying in 10 seconds")
        print(" | ✅ YouTube JSON!")

        if DEBUG:
            print(f" | Full API GET URL: {YOUTUBE_SOURCE}")
            print(f" | Full API Dump: {youtube_json}")

        # Key:Value RESPONSES
        if "pageInfo" in youtube_json:
            totalResults = youtube_json["pageInfo"]["totalResults"]
            print(f" |  | Matching Results: {totalResults}")

        if "items" in youtube_json:
            YT_request_kind = youtube_json["items"][0]["kind"]
            print(f" |  | Request Kind: {YT_request_kind}")

            YT_channel_id = youtube_json["items"][0]["id"]
            print(f" |  | Channel ID: {YT_channel_id}")

            YT_videoCount = youtube_json["items"][0]["statistics"]["videoCount"]
            print(f" |  | Videos: {YT_videoCount}")

            YT_viewCount = youtube_json["items"][0]["statistics"]["viewCount"]
            print(f" |  | Views: {YT_viewCount}")

            YT_subsCount = youtube_json["items"][0]["statistics"]["subscriberCount"]
            print(f" |  | Subscribers: {YT_subsCount}")

        if "kind" in youtube_json:
            YT_response_kind = youtube_json["kind"]
            print(f" |  | Response Kind: {YT_response_kind}")

        print("\nFinished!")
        print(f"Board Uptime: {time_calc(time.monotonic())}")
        print(f"Next Update: {time_calc(SLEEP_TIME)}")
        print("===============================")

    except (ValueError, RuntimeError) as e:
        print(f"Failed to get data, retrying\n {e}")
        time.sleep(60)
        break
    time.sleep(SLEEP_TIME)
