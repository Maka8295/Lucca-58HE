# SPDX-FileCopyrightText: 2024 DJDevon3
# SPDX-License-Identifier: MIT
# Coded for Circuit Python 8.2.x
"""Fitbit API Example"""
# pylint: disable=no-member

import os
import time

import adafruit_connection_manager
import microcontroller
import wifi

import adafruit_requests

# --- Fitbit Developer Account & oAuth App Required: ---
# Required: Google Login (Fitbit owned by Google) & Fitbit Device
# Step 1: Register a personal app here: https://dev.fitbit.com
# Step 2: Use their Tutorial to get the Token and first Refresh Token
# Fitbit's Tutorial Step 4 is as far as you need to go.
# https://dev.fitbit.com/build/reference/web-api/troubleshooting-guide/oauth2-tutorial/

# Ensure these are in settings.toml
# Fitbit_ClientID = "YourAppClientID"
# Fitbit_Token = "Long 256 character string (SHA-256)"
# Fitbit_First_Refresh_Token = "64 character string"
# Fitbit_UserID = "UserID authorizing the ClientID"

# Get WiFi details, ensure these are setup in settings.toml
ssid = os.getenv("CIRCUITPY_WIFI_SSID")
password = os.getenv("CIRCUITPY_WIFI_PASSWORD")
Fitbit_ClientID = os.getenv("FITBIT_CLIENTID")
Fitbit_Token = os.getenv("FITBIT_ACCESS_TOKEN")
Fitbit_First_Refresh_Token = os.getenv(
    "FITBIT_FIRST_REFRESH_TOKEN"
)  # overides nvm first run only
Fitbit_UserID = os.getenv("FITBIT_USERID")

# Set debug to True for full INTRADAY JSON response.
# WARNING: may include visible credentials
# MICROCONTROLLER WARNING: might crash by returning too much data
DEBUG = False

# Set debug to True for full DEVICE (Watch) JSON response.
# WARNING: may include visible credentials
# This will not return enough data to crash your device.
DEBUG_DEVICE = False

# No data from midnight to 00:15 due to lack of 15 values.
# Debug midnight to display something else in this time frame.
MIDNIGHT_DEBUG = False

# WARNING: Optional: Resets board nvm to factory default. Clean slate.
# Instructions will be printed to console while reset is True.
RESET_NVM = False  # Set True once, then back to False
if RESET_NVM:
    microcontroller.nvm[0:64] = bytearray(b"\x00" * 64)
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


# Authenticates Client ID & SHA-256 Token to POST
FITBIT_OAUTH_HEADER = {"Content-Type": "application/x-www-form-urlencoded"}
FITBIT_OAUTH_TOKEN = "https://api.fitbit.com/oauth2/token"

# Use to confirm first instance of NVM is the correct refresh token
FIRST_RUN = True
Refresh_Token = Fitbit_First_Refresh_Token
top_nvm = microcontroller.nvm[0:64].decode()
nvm_bytes = microcontroller.nvm[0:64]
top_nvm_3bytes = nvm_bytes[0:3]
if DEBUG:
    print(f"Top NVM Length: {len(top_nvm)}")
    print(f"Top NVM: {top_nvm}")
    print(f"Top NVM bytes: {top_nvm_3bytes}")
if RESET_NVM:
    microcontroller.nvm[0:64] = bytearray(b"\x00" * 64)
    if top_nvm_3bytes == b"\x00\x00\x00":
        print("TOP NVM IS BRAND NEW! WAITING FOR A FIRST TOKEN")
        Fitbit_First_Refresh_Token = top_nvm
        print(f"Top NVM RESET: {top_nvm}")  # No token should appear
        Refresh_Token = microcontroller.nvm[0:64].decode()
        print(f"Refresh_Token Reset: {Refresh_Token}")  # No token should appear
while True:
    if not RESET_NVM:
        # Connect to Wi-Fi
        print("\n📡 Connecting to WiFi...")
        while not wifi.radio.ipv4_address:
            try:
                wifi.radio.connect(ssid, password)
            except ConnectionError as e:
                print("❌ Connection Error:", e)
                print("Retrying in 10 seconds")
        print("✅ WiFi!")

        if top_nvm is not Refresh_Token and FIRST_RUN is False:
            FIRST_RUN = False
            Refresh_Token = microcontroller.nvm[0:64].decode()
            print(" | INDEFINITE RUN -------")
            if DEBUG:
                print("Top NVM is Fitbit First Refresh Token")
                # NVM 64 should match Current Refresh Token
                print(f"NVM 64: {microcontroller.nvm[0:64].decode()}")
                print(f"Current Refresh_Token: {Refresh_Token}")
        if top_nvm != Fitbit_First_Refresh_Token and FIRST_RUN is True:
            if top_nvm_3bytes == b"\x00\x00\x00":
                print(" | TOP NVM IS BRAND NEW! WAITING FOR A FIRST TOKEN")
                Refresh_Token = Fitbit_First_Refresh_Token
                nvmtoken = b"" + Refresh_Token
                microcontroller.nvm[0:64] = nvmtoken
            else:
                if DEBUG:
                    print(f"Top NVM: {top_nvm}")
                    print(f"First Refresh: {Refresh_Token}")
                    print(f"First Run: {FIRST_RUN}")
                Refresh_Token = top_nvm
                FIRST_RUN = False
                print(" | MANUAL REBOOT TOKEN DIFFERENCE -------")
                if DEBUG:
                    # NVM 64 should not match Current Refresh Token
                    print("Top NVM is NOT Fitbit First Refresh Token")
                    print(f"NVM 64: {microcontroller.nvm[0:64].decode()}")
                    print(f"Current Refresh_Token: {Refresh_Token}")
        if top_nvm == Refresh_Token and FIRST_RUN is True:
            if DEBUG:
                print(f"Top NVM: {top_nvm}")
                print(f"First Refresh: {Refresh_Token}")
                print(f"First Run: {FIRST_RUN}")
            Refresh_Token = Fitbit_First_Refresh_Token
            nvmtoken = b"" + Refresh_Token
            microcontroller.nvm[0:64] = nvmtoken
            FIRST_RUN = False
            print(" | FIRST RUN SETTINGS.TOML TOKEN-------")
            if DEBUG:
                # NVM 64 should match Current Refresh Token
                print("Top NVM IS Fitbit First Refresh Token")
                print(f"NVM 64: {microcontroller.nvm[0:64].decode()}")
                print(f"Current Refresh_Token: {Refresh_Token}")
        try:
            if DEBUG:
                print("\n-----Token Refresh POST Attempt -------")
            FITBIT_OAUTH_REFRESH_TOKEN = (
                "&grant_type=refresh_token"
                + "&client_id="
                + str(Fitbit_ClientID)
                + "&refresh_token="
                + str(Refresh_Token)
            )

            # ------------------------- POST FOR REFRESH TOKEN --------------------
            print(" | Requesting authorization for next token")
            if DEBUG:
                print(
                    "FULL REFRESH TOKEN POST:"
                    + f"{FITBIT_OAUTH_TOKEN}{FITBIT_OAUTH_REFRESH_TOKEN}"
                )
                print(f"Current Refresh Token: {Refresh_Token}")
            # TOKEN REFRESH POST
            try:
                with requests.post(
                    url=FITBIT_OAUTH_TOKEN,
                    data=FITBIT_OAUTH_REFRESH_TOKEN,
                    headers=FITBIT_OAUTH_HEADER,
                ) as fitbit_oauth_refresh_POST:
                    fitbit_refresh_oauth_json = fitbit_oauth_refresh_POST.json()
            except adafruit_requests.OutOfRetries as ex:
                print(f"OutOfRetries: {ex}")
                break
            try:
                fitbit_new_token = fitbit_refresh_oauth_json["access_token"]
                if DEBUG:
                    print("Your Private SHA-256 Token: ", fitbit_new_token)
                fitbit_access_token = fitbit_new_token  # NEW FULL TOKEN

                # Overwrites Initial/Old Refresh Token with Next/New Refresh Token
                fitbit_new_refesh_token = fitbit_refresh_oauth_json["refresh_token"]
                Refresh_Token = fitbit_new_refesh_token

                fitbit_token_expiration = fitbit_refresh_oauth_json["expires_in"]
                fitbit_scope = fitbit_refresh_oauth_json["scope"]
                fitbit_token_type = fitbit_refresh_oauth_json["token_type"]
                fitbit_user_id = fitbit_refresh_oauth_json["user_id"]
                if DEBUG:
                    print("Next Refresh Token: ", Refresh_Token)
                try:
                    # Stores Next token in NVM
                    nvmtoken = b"" + Refresh_Token
                    microcontroller.nvm[0:64] = nvmtoken
                    if DEBUG:
                        print(f"nvmtoken: {nvmtoken}")
                    # It's better to always have next token visible.
                    # You can manually set this token into settings.toml
                    print(f" | Next Token: {nvmtoken.decode()}")
                    print(" | 🔑 Next token written to NVM Successfully!")
                except OSError as e:
                    print("OS Error:", e)
                    continue
                if DEBUG:
                    print("Token Expires in: ", time_calc(fitbit_token_expiration))
                    print("Scope: ", fitbit_scope)
                    print("Token Type: ", fitbit_token_type)
                    print("UserID: ", fitbit_user_id)
            except KeyError as e:
                print("Key Error:", e)
                print("Expired token, invalid permission, or (key:value) pair error.")
                time.sleep(SLEEP_TIME)
                continue
            # ----------------------------- GET DATA ---------------------------------
            # Now that we have POST response with next refresh token we can GET for data
            # 64-bit Refresh tokens will "keep alive" SHA-256 token indefinitely
            # Fitbit main SHA-256 token expires in 8 hours unless refreshed!
            # ------------------------------------------------------------------------
            DETAIL_LEVEL = "1min"  # Supported: 1sec | 1min | 5min | 15min
            REQUESTED_DATE = "today"  # Date format yyyy-MM-dd or "today"
            fitbit_header = {
                "Authorization": "Bearer " + fitbit_access_token + "",
                "Client-Id": "" + Fitbit_ClientID + "",
            }
            # Heart Intraday Scope
            FITBIT_INTRADAY_SOURCE = (
                "https://api.fitbit.com/1/user/"
                + Fitbit_UserID
                + "/activities/heart/date/"
                + REQUESTED_DATE
                + "/1d/"
                + DETAIL_LEVEL
                + ".json"
            )
            # Device Details
            FITBIT_DEVICE_SOURCE = (
                "https://api.fitbit.com/1/user/" + Fitbit_UserID + "/devices.json"
            )

            print(" | Attempting to GET Fitbit JSON!")
            FBIS = FITBIT_INTRADAY_SOURCE
            FBH = fitbit_header
            try:
                with requests.get(url=FBIS, headers=FBH) as fitbit_get_response:
                    fitbit_json = fitbit_get_response.json()
            except ConnectionError as e:
                print("Connection Error:", e)
                print("Retrying in 10 seconds")
            print(" | ✅ Fitbit Intraday JSON!")

            if DEBUG:
                print(f"Full API GET URL: {FBIS}")
                print(f"Header: {fitbit_header}")
                # This might crash your microcontroller.
                # Commented out even in debug. Use only if absolutely necessary.

                # print(f"JSON Full Response: {fitbit_json}")
                Intraday_Response = fitbit_json["activities-heart-intraday"]["dataset"]
                # print(f"Intraday Full Response: {Intraday_Response}")
            try:
                # Fitbit's sync to mobile device & server every 15 minutes in chunks.
                # Pointless to poll their API faster than 15 minute intervals.
                activities_heart_value = fitbit_json["activities-heart-intraday"][
                    "dataset"
                ]
                if MIDNIGHT_DEBUG:
                    RESPONSE_LENGTH = 0
                else:
                    RESPONSE_LENGTH = len(activities_heart_value)
                if RESPONSE_LENGTH >= 15:
                    activities_timestamp = fitbit_json["activities-heart"][0][
                        "dateTime"
                    ]
                    print(f" |  | Fitbit Date: {activities_timestamp}")
                    if MIDNIGHT_DEBUG:
                        ACTIVITIES_LATEST_HEART_TIME = str("00:05:00")
                    else:
                        ACTIVITIES_LATEST_HEART_TIME = fitbit_json[
                            "activities-heart-intraday"
                        ]["dataset"][RESPONSE_LENGTH - 1]["time"]
                    print(f" |  | Fitbit Time: {ACTIVITIES_LATEST_HEART_TIME[0:-3]}")
                    print(f" |  | Today's Logged Pulses: {RESPONSE_LENGTH}")

                    # Each 1min heart rate is a 60 second average
                    LATEST_15_AVG = " |  | Latest 15 Minute Averages: "
                    LATEST_15_VALUES = ", ".join(
                        str(activities_heart_value[i]["value"])
                        for i in range(RESPONSE_LENGTH - 1, RESPONSE_LENGTH - 16, -1)
                    )
                    print(f"{LATEST_15_AVG}{LATEST_15_VALUES}")
                else:
                    print(" | Waiting for latest sync...")
                    print(" | ❌ Not enough values for today to display yet.")
            except KeyError as keyerror:
                print(f"Key Error: {keyerror}")
                print(
                    "Too Many Requests, "
                    + "Expired token, "
                    + "invalid permission, "
                    + "or (key:value) pair error."
                )
                time.sleep(60)
                continue
            # Getting Fitbit Device JSON (separate from intraday)
            # Separate call for Watch Battery Percentage.
            print(" | Attempting to GET Device JSON!")
            FBDS = FITBIT_DEVICE_SOURCE
            FBH = fitbit_header
            try:
                with requests.get(url=FBDS, headers=FBH) as fitbit_get_device_response:
                    fitbit_device_json = fitbit_get_device_response.json()
            except ConnectionError as e:
                print("Connection Error:", e)
                print("Retrying in 10 seconds")
            print(" | ✅ Fitbit Device JSON!")

            if DEBUG_DEVICE:
                print(f"Full API GET URL: {FITBIT_DEVICE_SOURCE}")
                print(f"Header: {fitbit_header}")
                print(f"JSON Full Response: {fitbit_device_json}")
            Device_Response = fitbit_device_json[1]["batteryLevel"]
            print(f" |  | Watch Battery %: {Device_Response}")

            print("\nFinished!")
            print(f"Board Uptime: {time_calc(time.monotonic())}")
            print(f"Next Update: {time_calc(SLEEP_TIME)}")
            print("===============================")
        except (ValueError, RuntimeError) as e:
            print("Failed to get data, retrying\n", e)
            time.sleep(60)
            continue
        time.sleep(SLEEP_TIME)
    else:
        print("🚮 NVM Cleared!")
        print(
            "⚠️ Save your new access token & refresh token from "
            "Fitbits Tutorial (Step 4) to settings.toml now."
        )
        print(
            "⚠️ If the script runs again"
            "(due to settings.toml file save) while reset=True that's ok!"
        )
        print("⚠️ Then set RESET_NVM back to False.")
        break
