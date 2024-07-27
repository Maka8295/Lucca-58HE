# SPDX-FileCopyrightText: 2024 DJDevon3
# SPDX-License-Identifier: MIT
# Coded for Circuit Python 9.x
"""Rachio Irrigation Timer API Example"""

import os
import time

import adafruit_connection_manager
import wifi

import adafruit_requests

# Rachio API Key required (comes with purchase of a device)
# API is rate limited to 1700 calls per day.
# https://support.rachio.com/en_us/public-api-documentation-S1UydL1Fv
# https://rachio.readme.io/reference/getting-started
RACHIO_KEY = os.getenv("RACHIO_APIKEY")
RACHIO_PERSONID = os.getenv("RACHIO_PERSONID")

# Get WiFi details, ensure these are setup in settings.toml
ssid = os.getenv("CIRCUITPY_WIFI_SSID")
password = os.getenv("CIRCUITPY_WIFI_PASSWORD")

# API Polling Rate
# 900 = 15 mins, 1800 = 30 mins, 3600 = 1 hour
SLEEP_TIME = 900

# Set debug to True for full JSON response.
# WARNING: absolutely shows extremely sensitive personal information & credentials
# Including your real name, latitude, longitude, account id, mac address, etc...
DEBUG = False

# Initalize Wifi, Socket Pool, Request Session
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)

RACHIO_HEADER = {"Authorization": " Bearer " + RACHIO_KEY}
RACHIO_SOURCE = "https://api.rach.io/1/public/person/info/"
RACHIO_PERSON_SOURCE = "https://api.rach.io/1/public/person/"


def obfuscating_asterix(obfuscate_object, direction, characters=2):
    """
    Obfuscates a string with asterisks except for a specified number of characters.
    param object: str The string to obfuscate with asterisks
    param direction: str Option either 'prepend', 'append', or 'all' direction
    param characters: int The number of characters to keep unobfuscated (default is 2)
    """
    object_len = len(obfuscate_object)
    if direction not in {"prepend", "append", "all"}:
        raise ValueError("Invalid direction. Use 'prepend', 'append', or 'all'.")
    if characters >= object_len and direction != "all":
        # If characters greater than or equal to string length,
        # return the original string as it can't be obfuscated.
        return obfuscate_object
    asterix_replace = "*" * object_len
    if direction == "append":
        asterix_final = obfuscate_object[:characters] + "*" * (object_len - characters)
    elif direction == "prepend":
        asterix_final = "*" * (object_len - characters) + obfuscate_object[-characters:]
    elif direction == "all":
        # Replace all characters with asterisks
        asterix_final = asterix_replace

    return asterix_final


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

    # RETREIVE PERSONID AND PASTE IT TO SETTINGS.TOML
    if RACHIO_PERSONID is None or RACHIO_PERSONID == "":
        try:
            print(" | Attempting to GET Rachio Authorization")
            try:
                with requests.get(
                    url=RACHIO_SOURCE, headers=RACHIO_HEADER
                ) as rachio_response:
                    rachio_json = rachio_response.json()
            except ConnectionError as e:
                print("Connection Error:", e)
                print("Retrying in 10 seconds")
            print(" | ✅ Authorized")

            rachio_id = rachio_json["id"]
            print("\nADD THIS 🔑 TO YOUR SETTINGS.TOML FILE!")
            print(f'RACHIO_PERSONID = "{rachio_id}"')

            if DEBUG:
                print("\nFull API GET URL: ", RACHIO_SOURCE)
                print(rachio_json)

        except (ValueError, RuntimeError) as e:
            print(f"Failed to GET data: {e}")
            time.sleep(60)
            break
        print(
            "\nThis script can only continue when a proper APIKey & PersonID is used."
        )
        print("\nFinished!")
        print("===============================")
        time.sleep(SLEEP_TIME)

    # Main Script
    if RACHIO_PERSONID is not None and RACHIO_PERSONID != "":
        try:
            print(" | Attempting to GET Rachio JSON")
            try:
                with requests.get(
                    url=RACHIO_PERSON_SOURCE + RACHIO_PERSONID, headers=RACHIO_HEADER
                ) as rachio_response:
                    rachio_json = rachio_response.json()
            except ConnectionError as e:
                print("Connection Error:", e)
                print("Retrying in 10 seconds")
            print(" | ✅ Rachio JSON")
            response_headers = rachio_response.headers
            if DEBUG:
                print(f"Response Headers: {response_headers}")
            call_limit = int(response_headers["x-ratelimit-limit"])
            calls_remaining = int(response_headers["x-ratelimit-remaining"])
            calls_made_today = call_limit - calls_remaining

            print(" |  | Headers:")
            print(f" |  |  | Date: {response_headers['date']}")
            print(f" |  |  | Maximum Daily Requests: {call_limit}")
            print(f" |  |  | Today's Requests: {calls_made_today}")
            print(f" |  |  | Remaining Requests: {calls_remaining}")
            print(f" |  |  | Limit Reset: {response_headers['x-ratelimit-reset']}")
            print(f" |  |  | Content Type: {response_headers['content-type']}")

            rachio_id = rachio_json["id"]
            rachio_id_ast = obfuscating_asterix(rachio_id, "append", 3)
            print(" |  | PersonID: ", rachio_id_ast)

            rachio_username = rachio_json["username"]
            rachio_username_ast = obfuscating_asterix(rachio_username, "append", 3)
            print(" |  | Username: ", rachio_username_ast)

            rachio_name = rachio_json["fullName"]
            rachio_name_ast = obfuscating_asterix(rachio_name, "append", 3)
            print(" |  | Full Name: ", rachio_name_ast)

            rachio_deleted = rachio_json["deleted"]
            if not rachio_deleted:
                print(" |  | Account Status: Active")
            else:
                print(" |  | Account Status?: Deleted!")

            rachio_createdate = rachio_json["createDate"]
            rachio_timezone_offset = rachio_json["devices"][0]["utcOffset"]
            # Rachio Unix time is in milliseconds, convert to seconds
            rachio_createdate_seconds = rachio_createdate // 1000
            rachio_timezone_offset_seconds = rachio_timezone_offset // 1000
            # Apply timezone offset in seconds
            local_unix_time = rachio_createdate_seconds + rachio_timezone_offset_seconds
            if DEBUG:
                print(f" |  | Unix Registration Date: {rachio_createdate}")
                print(f" |  | Unix Timezone Offset: {rachio_timezone_offset}")
            current_struct_time = time.localtime(local_unix_time)
            final_timestamp = "{}".format(_format_datetime(current_struct_time))
            print(f" |  | Registration Date: {final_timestamp}")

            rachio_devices = rachio_json["devices"][0]["name"]
            print(" |  | Device: ", rachio_devices)

            rachio_model = rachio_json["devices"][0]["model"]
            print(" |  |  | Model: ", rachio_model)

            rachio_serial = rachio_json["devices"][0]["serialNumber"]
            rachio_serial_ast = obfuscating_asterix(rachio_serial, "append")
            print(" |  |  | Serial Number: ", rachio_serial_ast)

            rachio_mac = rachio_json["devices"][0]["macAddress"]
            rachio_mac_ast = obfuscating_asterix(rachio_mac, "append")
            print(" |  |  | MAC Address: ", rachio_mac_ast)

            rachio_status = rachio_json["devices"][0]["status"]
            print(" |  |  | Device Status: ", rachio_status)

            rachio_timezone = rachio_json["devices"][0]["timeZone"]
            print(" |  |  | Time Zone: ", rachio_timezone)

            # Latitude & Longtitude are used for smart watering & rain delays
            rachio_latitude = str(rachio_json["devices"][0]["latitude"])
            rachio_lat_ast = obfuscating_asterix(rachio_latitude, "all")
            print(" |  |  | Latitude: ", rachio_lat_ast)

            rachio_longitude = str(rachio_json["devices"][0]["longitude"])
            rachio_long_ast = obfuscating_asterix(rachio_longitude, "all")
            print(" |  |  | Longitude: ", rachio_long_ast)

            rachio_rainsensor = rachio_json["devices"][0]["rainSensorTripped"]
            print(" |  |  | Rain Sensor: ", rachio_rainsensor)

            rachio_zone0 = rachio_json["devices"][0]["zones"][0]["name"]
            rachio_zone1 = rachio_json["devices"][0]["zones"][1]["name"]
            rachio_zone2 = rachio_json["devices"][0]["zones"][2]["name"]
            rachio_zone3 = rachio_json["devices"][0]["zones"][3]["name"]
            zones = f"{rachio_zone0}, {rachio_zone1}, {rachio_zone2}, {rachio_zone3}"
            print(f" |  |  | Zones: {zones}")

            if DEBUG:
                print(f"\nFull API GET URL: {RACHIO_PERSON_SOURCE+rachio_id}")
                print(rachio_json)

            print("\nFinished!")
            print(f"Board Uptime: {time_calc(time.monotonic())}")
            print(f"Next Update: {time_calc(SLEEP_TIME)}")
            print("===============================")

        except (ValueError, RuntimeError) as e:
            print(f"Failed to get data, retrying\n {e}")
            time.sleep(60)
            break

        time.sleep(SLEEP_TIME)
