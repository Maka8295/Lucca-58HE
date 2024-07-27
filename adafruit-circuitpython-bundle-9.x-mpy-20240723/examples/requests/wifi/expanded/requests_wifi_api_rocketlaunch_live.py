# SPDX-FileCopyrightText: 2024 DJDevon3
# SPDX-License-Identifier: MIT
# Coded for Circuit Python 9.0
"""RocketLaunch.Live API Example"""

import os
import time

import adafruit_connection_manager
import wifi

import adafruit_requests

# Time between API refreshes
# 900 = 15 mins, 1800 = 30 mins, 3600 = 1 hour
SLEEP_TIME = 43200

# Get WiFi details, ensure these are setup in settings.toml
ssid = os.getenv("CIRCUITPY_WIFI_SSID")
password = os.getenv("CIRCUITPY_WIFI_PASSWORD")


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
# The number at the end is the amount of launches (max 5 free api)
ROCKETLAUNCH_SOURCE = "https://fdo.rocketlaunch.live/json/launches/next/1"

# Initalize Wifi, Socket Pool, Request Session
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)

while True:
    # Connect to Wi-Fi
    print("\n===============================")
    print("Connecting to WiFi...")
    while not wifi.radio.ipv4_address:
        try:
            wifi.radio.connect(ssid, password)
        except ConnectionError as e:
            print("❌ Connection Error:", e)
            print("Retrying in 10 seconds")
    print("✅ Wifi!")
    try:
        # Print Request to Serial
        print(" | Attempting to GET RocketLaunch.Live JSON!")
        time.sleep(2)
        debug_rocketlaunch_full_response = False

        try:
            with requests.get(url=ROCKETLAUNCH_SOURCE) as rocketlaunch_response:
                rocketlaunch_json = rocketlaunch_response.json()
        except ConnectionError as e:
            print("Connection Error:", e)
            print("Retrying in 10 seconds")
        print(" | ✅ RocketLaunch.Live JSON!")

        if debug_rocketlaunch_full_response:
            print("Full API GET URL: ", ROCKETLAUNCH_SOURCE)
            print(rocketlaunch_json)

        # JSON Endpoints
        RLFN = str(rocketlaunch_json["result"][0]["name"])
        RLWO = str(rocketlaunch_json["result"][0]["win_open"])
        TZERO = str(rocketlaunch_json["result"][0]["t0"])
        RLWC = str(rocketlaunch_json["result"][0]["win_close"])
        RLP = str(rocketlaunch_json["result"][0]["provider"]["name"])
        RLVN = str(rocketlaunch_json["result"][0]["vehicle"]["name"])
        RLPN = str(rocketlaunch_json["result"][0]["pad"]["name"])
        RLLS = str(rocketlaunch_json["result"][0]["pad"]["location"]["name"])
        RLLD = str(rocketlaunch_json["result"][0]["launch_description"])
        RLM = str(rocketlaunch_json["result"][0]["mission_description"])
        RLDATE = str(rocketlaunch_json["result"][0]["date_str"])

        # Print to serial & display label if endpoint not "None"
        if RLDATE != "None":
            print(f" |  | Date: {RLDATE}")
        if RLFN != "None":
            print(f" |  | Flight: {RLFN}")
        if RLP != "None":
            print(f" |  | Provider: {RLP}")
        if RLVN != "None":
            print(f" |  | Vehicle: {RLVN}")

        # Launch time can sometimes be Window Open to Close, T-Zero, or weird combination.
        # Should obviously be standardized but they're not input that way.
        # Have to account for every combination of 3 conditions.
        # T-Zero Launch Time Conditionals
        if RLWO == "None" and TZERO != "None" and RLWC != "None":
            print(f" |  | Window: {TZERO} | {RLWC}")
        elif RLWO != "None" and TZERO != "None" and RLWC == "None":
            print(f" |  | Window: {RLWO} | {TZERO}")
        elif RLWO != "None" and TZERO == "None" and RLWC != "None":
            print(f" |  | Window: {RLWO} | {RLWC}")
        elif RLWO != "None" and TZERO != "None" and RLWC != "None":
            print(f" |  | Window: {RLWO} | {TZERO} | {RLWC}")
        elif RLWO == "None" and TZERO != "None" and RLWC == "None":
            print(f" |  | Window: {TZERO}")
        elif RLWO != "None" and TZERO == "None" and RLWC == "None":
            print(f" |  | Window: {RLWO}")
        elif RLWO == "None" and TZERO == "None" and RLWC != "None":
            print(f" |  | Window: {RLWC}")

        if RLLS != "None":
            print(f" |  | Site: {RLLS}")
        if RLPN != "None":
            print(f" |  | Pad: {RLPN}")
        if RLLD != "None":
            print(f" |  | Description: {RLLD}")
        if RLM != "None":
            print(f" |  | Mission: {RLM}")

        print("\nFinished!")
        print(f"Board Uptime: {time_calc(time.monotonic())}")
        print(f"Next Update: {time_calc(SLEEP_TIME)}")
        print("===============================")

    except (ValueError, RuntimeError) as e:
        print("Failed to get data, retrying\n", e)
        time.sleep(60)
        break
    time.sleep(SLEEP_TIME)
