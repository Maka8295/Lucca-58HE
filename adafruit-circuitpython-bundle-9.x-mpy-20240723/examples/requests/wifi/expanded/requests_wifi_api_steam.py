# SPDX-FileCopyrightText: 2024 DJDevon3
# SPDX-License-Identifier: MIT
# Coded for Circuit Python 8.2.x
"""Steam API Get Owned Games Example"""

import os
import time

import adafruit_connection_manager
import wifi

import adafruit_requests

# Steam API Docs: https://steamcommunity.com/dev
# Steam API Key: https://steamcommunity.com/dev/apikey
# Numerical Steam ID: Visit https://store.steampowered.com/account/
# Your account name will be in big bold letters.
# Your numerical STEAM ID will be below in a very small font.

# Get WiFi details, ensure these are setup in settings.toml
ssid = os.getenv("CIRCUITPY_WIFI_SSID")
password = os.getenv("CIRCUITPY_WIFI_PASSWORD")
# Requires Steam Developer API key
steam_usernumber = os.getenv("STEAM_ID")
steam_apikey = os.getenv("STEAM_API_KEY")

# API Polling Rate
# 900 = 15 mins, 1800 = 30 mins, 3600 = 1 hour
SLEEP_TIME = 3600

# Set debug to True for full JSON response.
# WARNING: Steam's full response will overload most microcontrollers
# SET TO TRUE IF YOU FEEL BRAVE =)
DEBUG = False

# Initalize Wifi, Socket Pool, Request Session
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)

# Deconstruct URL (pylint hates long lines)
# http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/
# ?key=XXXXXXXXXXXXXXXXXXXXX&include_played_free_games=1&steamid=XXXXXXXXXXXXXXXX&format=json
STEAM_SOURCE = (
    "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?"
    + "key="
    + steam_apikey
    + "&include_played_free_games=1"
    + "&steamid="
    + steam_usernumber
    + "&format=json"
)


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
        print(" | Attempting to GET Steam API JSON!")
        try:
            with requests.get(url=STEAM_SOURCE) as steam_response:
                steam_json = steam_response.json()
        except ConnectionError as e:
            print("Connection Error:", e)
            print("Retrying in 10 seconds")

        print(" | ✅ Steam JSON!")

        if DEBUG:
            print("Full API GET URL: ", STEAM_SOURCE)
            print(steam_json)

        game_count = steam_json["response"]["game_count"]
        print(f" |  | Total Games: {game_count}")
        TOTAL_MINUTES = 0

        for game in steam_json["response"]["games"]:
            TOTAL_MINUTES += game["playtime_forever"]
        total_hours = TOTAL_MINUTES / 60
        total_days = TOTAL_MINUTES / 60 / 24
        total_years = TOTAL_MINUTES / 60 / 24 / 365
        print(f" |  | Total Hours: {total_hours}")
        print(f" |  | Total Days:  {total_days}")
        print(f" |  | Total Years: {total_years:.2f}")

        print("\nFinished!")
        print(f"Board Uptime: {time_calc(time.monotonic())}")
        print(f"Next Update: {time_calc(SLEEP_TIME)}")
        print("===============================")

    except (ValueError, RuntimeError) as e:
        print(f"Failed to get data, retrying\n {e}")
        time.sleep(60)
        break
    time.sleep(SLEEP_TIME)
