# SPDX-FileCopyrightText: 2024 DJDevon3
# SPDX-License-Identifier: MIT
# Coded for Circuit Python 9.x
"""OpenSky-Network.org Single Flight Public API Example"""

import os
import time

import adafruit_connection_manager
import wifi

import adafruit_requests

# No login necessary for Public API. Drastically reduced daily limit vs Private
# OpenSky-Networks.org REST API: https://openskynetwork.github.io/opensky-api/rest.html
# All active flights JSON: https://opensky-network.org/api/states/all PICK ONE!
# JSON order: transponder, callsign, country
# ACTIVE transpondes only, for multiple "c822af&icao24=cb3993&icao24=c63923"
TRANSPONDER = "88044d"

# Get WiFi details, ensure these are setup in settings.toml
ssid = os.getenv("CIRCUITPY_WIFI_SSID")
password = os.getenv("CIRCUITPY_WIFI_PASSWORD")

# API Polling Rate
# 900 = 15 mins, 1800 = 30 mins, 3600 = 1 hour
# OpenSky-Networks IP bans for too many requests, check rate limit.
# https://openskynetwork.github.io/opensky-api/rest.html#limitations
SLEEP_TIME = 1800

# Set debug to True for full JSON response.
# WARNING: makes credentials visible
DEBUG = False

# Initalize Wifi, Socket Pool, Request Session
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)

# Requests URL - icao24 is their endpoint required for a transponder
# example https://opensky-network.org/api/states/all?icao24=a808c5
OPENSKY_SOURCE = "https://opensky-network.org/api/states/all?" + "icao24=" + TRANSPONDER


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
        print(" | Attempting to GET OpenSky-Network Single Public Flight JSON!")
        print(" | Website Credentials NOT Required! Less daily calls than Private.")
        try:
            with requests.get(url=OPENSKY_SOURCE) as opensky_response:
                opensky_json = opensky_response.json()
        except ConnectionError as e:
            print("Connection Error:", e)
            print("Retrying in 10 seconds")

        print(" | ✅ OpenSky-Network Public JSON!")

        if DEBUG:
            print("Full API GET URL: ", OPENSKY_SOURCE)
            print(opensky_json)

        # ERROR MESSAGE RESPONSES
        if "timestamp" in opensky_json:
            osn_timestamp = opensky_json["timestamp"]
            print(f"❌ Timestamp: {osn_timestamp}")

        if "message" in opensky_json:
            osn_message = opensky_json["message"]
            print(f"❌ Message: {osn_message}")

        if "error" in opensky_json:
            osn_error = opensky_json["error"]
            print(f"❌ Error: {osn_error}")

        if "path" in opensky_json:
            osn_path = opensky_json["path"]
            print(f"❌ Path: {osn_path}")

        if "status" in opensky_json:
            osn_status = opensky_json["status"]
            print(f"❌ Status: {osn_status}")

        # Current flight data for single callsign (right now)
        osn_single_flight_data = opensky_json["states"]

        if osn_single_flight_data is not None:
            if DEBUG:
                print(f" |  | Single Flight Public Data: {osn_single_flight_data}")

            last_contact = opensky_json["states"][0][4]
            # print(f" |  | Last Contact Unix Time: {last_contact}")
            lc_struct_time = time.localtime(last_contact)
            lc_readable_time = f"{_format_datetime(lc_struct_time)}"
            print(f" |  | Last Contact: {lc_readable_time}")

            flight_transponder = opensky_json["states"][0][0]
            print(f" |  | Transponder: {flight_transponder}")

            callsign = opensky_json["states"][0][1]
            print(f" |  | Callsign: {callsign}")

            squawk = opensky_json["states"][0][14]
            print(f" |  | Squawk: {squawk}")

            country = opensky_json["states"][0][2]
            print(f" |  | Origin: {country}")

            longitude = opensky_json["states"][0][5]
            print(f" |  | Longitude: {longitude}")

            latitude = opensky_json["states"][0][6]
            print(f" |  | Latitude: {latitude}")

            # Return Air Flight data if not on ground
            on_ground = opensky_json["states"][0][8]
            if on_ground is True:
                print(f" |  | On Ground: {on_ground}")
            else:
                altitude = opensky_json["states"][0][7]
                print(f" |  | Barometric Altitude: {altitude}")

                velocity = opensky_json["states"][0][9]
                if velocity != "null":
                    print(f" |  | Velocity: {velocity}")

                vertical_rate = opensky_json["states"][0][11]
                if vertical_rate != "null":
                    print(f" |  | Vertical Rate: {vertical_rate}")
        else:
            print("This flight has no active data or you're polling too fast.")
            print("Public Limits: 10 second max poll & 400 weighted calls daily")

        print("\nFinished!")
        print(f"Board Uptime: {time_calc(time.monotonic())}")
        print(f"Next Update: {time_calc(SLEEP_TIME)}")
        print("===============================")

    except (ValueError, RuntimeError) as e:
        print(f"Failed to get data, retrying\n {e}")
        time.sleep(60)
        break
    time.sleep(SLEEP_TIME)
