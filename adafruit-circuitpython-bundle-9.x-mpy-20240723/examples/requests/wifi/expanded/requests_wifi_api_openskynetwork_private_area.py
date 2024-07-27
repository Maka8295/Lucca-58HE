# SPDX-FileCopyrightText: 2024 DJDevon3
# SPDX-License-Identifier: MIT
# Coded for Circuit Python 8.2.x
"""OpenSky-Network.org Private Area API Example"""

import binascii
import os
import time

import adafruit_connection_manager
import wifi

import adafruit_requests

# OpenSky-Network.org Website Login required for this API
# Increased call limit vs Public.
# REST API: https://openskynetwork.github.io/opensky-api/rest.html
# Retrieves all traffic within a geographic area (Orlando example)
LATMIN = "27.22"  # east bounding box
LATMAX = "28.8"  # west bounding box
LONMIN = "-81.46"  # north bounding box
LONMAX = "-80.40"  # south bounding box

# Get WiFi details, ensure these are setup in settings.toml
ssid = os.getenv("CIRCUITPY_WIFI_SSID")
password = os.getenv("CIRCUITPY_WIFI_PASSWORD")
osnusername = os.getenv("OSN_USERNAME")  # Website Credentials
osnpassword = os.getenv("OSN_PASSWORD")  # Website Credentials

# API Polling Rate
# 900 = 15 mins, 1800 = 30 mins, 3600 = 1 hour
# OpenSky-Networks IP bans for too many requests, check rate limit.
# https://openskynetwork.github.io/opensky-api/rest.html#limitations
SLEEP_TIME = 1800

# Set debug to True for full JSON response.
# WARNING: makes credentials visible. based on how many flights
# in your area, full response could crash microcontroller
DEBUG = False

# Initalize Wifi, Socket Pool, Request Session
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)

# -- Base64 Conversion --
OSN_CREDENTIALS = str(osnusername) + ":" + str(osnpassword)
# base64 encode and strip appended \n from bytearray
OSN_CREDENTIALS_B = binascii.b2a_base64(OSN_CREDENTIALS.encode()).strip()
BASE64_STRING = OSN_CREDENTIALS_B.decode()  # bytearray

if DEBUG:
    print("Base64 ByteArray: ", BASE64_STRING)

# Area requires OpenSky-Network.org username:password to be base64 encoded
OSN_HEADER = {"Authorization": "Basic " + BASE64_STRING}

# Example request of all traffic over Florida.
# Geographic areas calls cost less against the limit.
# https://opensky-network.org/api/states/all?lamin=25.21&lomin=-84.36&lamax=30.0&lomax=-78.40
OPENSKY_SOURCE = (
    "https://opensky-network.org/api/states/all?"
    + "lamin="
    + LATMIN
    + "&lomin="
    + LONMIN
    + "&lamax="
    + LATMAX
    + "&lomax="
    + LONMAX
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
        print(" | Attempting to GET OpenSky-Network Area Flights JSON!")
        try:
            with requests.get(
                url=OPENSKY_SOURCE, headers=OSN_HEADER
            ) as opensky_response:
                opensky_json = opensky_response.json()
        except ConnectionError as e:
            print("Connection Error:", e)
            print("Retrying in 10 seconds")

        print(" | ✅ OpenSky-Network JSON!")

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
        osn_all_flights = opensky_json["states"]

        if osn_all_flights is not None:
            if DEBUG:
                print(f" |  | Area Flights Full Response: {osn_all_flights}")

            osn_time = opensky_json["time"]
            # print(f" |  | Last Contact Unix Time: {osn_time}")
            osn_struct_time = time.localtime(osn_time)
            osn_readable_time = f"{_format_datetime(osn_struct_time)}"
            print(f" |  | Timestamp: {osn_readable_time}")

            if osn_all_flights is not None:
                # print("Flight Data: ", osn_all_flights)
                for flights in osn_all_flights:
                    osn_t = f" |  | Trans:{flights[0]} "
                    osn_c = f"Sign:{flights[1]}"
                    osn_o = f"Origin:{flights[2]} "
                    osn_tm = f"Time:{flights[3]} "
                    osn_l = f"Last:{flights[4]} "
                    osn_lo = f"Lon:{flights[5]} "
                    osn_la = f"Lat:{flights[6]} "
                    osn_ba = f"BaroAlt:{flights[7]} "
                    osn_g = f"Ground:{flights[8]} "
                    osn_v = f"Vel:{flights[9]} "
                    osn_h = f"Head:{flights[10]} "
                    osn_vr = f"VertRate:{flights[11]} "
                    osn_s = f"Sens:{flights[12]} "
                    osn_ga = f"GeoAlt:{flights[13]} "
                    osn_sq = f"Squawk:{flights[14]} "
                    osn_pr = f"Task:{flights[15]} "
                    osn_ps = f"PosSys:{flights[16]} "
                    osn_ca = f"Cat:{flights[16]} "
                    # This is just because pylint complains about long lines
                    string1 = f"{osn_t}{osn_c}{osn_o}{osn_tm}{osn_l}{osn_lo}"
                    string2 = f"{osn_la}{osn_ba}{osn_g}{osn_v}{osn_h}{osn_vr}"
                    string3 = f"{osn_s}{osn_ga}{osn_sq}{osn_pr}{osn_ps}{osn_ca}"
                    print(f"{string1}{string2}{string3}")

        else:
            print(" |  | ❌ Area has no active data or you're polling too fast.")

        print("\nFinished!")
        print(f"Board Uptime: {time_calc(time.monotonic())}")
        print(f"Next Update: {time_calc(SLEEP_TIME)}")
        print("===============================")

    except (ValueError, RuntimeError) as e:
        print(f"Failed to get data, retrying\n {e}")
        time.sleep(60)
        break
    time.sleep(SLEEP_TIME)
