# SPDX-FileCopyrightText: 2024 DJDevon3
# SPDX-License-Identifier: MIT
# Updated for Circuit Python 9.0
# https://help.openai.com/en/articles/6825453-chatgpt-release-notes
# https://chat.openai.com/share/32ef0c5f-ac92-4d36-9d1e-0f91e0c4c574
""" WiFi Status Codes Example """

import os
import time

import adafruit_connection_manager
import wifi

import adafruit_requests

# Get WiFi details, ensure these are setup in settings.toml
ssid = os.getenv("CIRCUITPY_WIFI_SSID")
password = os.getenv("CIRCUITPY_WIFI_PASSWORD")

# Initalize Wifi, Socket Pool, Request Session
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)
rssi = wifi.radio.ap_info.rssi


def print_http_status(expected_code, actual_code, description):
    """Returns HTTP status code and description"""
    if "100" <= actual_code <= "103":
        print(
            f" | ✅ Status Test Expected: {expected_code} Actual: {actual_code} - {description}"
        )
    elif "200" == actual_code:
        print(
            f" | 🆗 Status Test Expected: {expected_code} Actual: {actual_code} - {description}"
        )
    elif "201" <= actual_code <= "299":
        print(
            f" | ✅ Status Test Expected: {expected_code} Actual: {actual_code} - {description}"
        )
    elif "300" <= actual_code <= "600":
        print(
            f" | ❌ Status Test Expected: {expected_code} Actual: {actual_code} - {description}"
        )
    else:
        print(
            f" | Unknown Response Status Expected: {expected_code} "
            + f"Actual: {actual_code} - {description}"
        )


# All HTTP Status Codes
http_status_codes = {
    "100": "Continue",
    "101": "Switching Protocols",
    "102": "Processing",
    "103": "Early Hints",
    "200": "OK",
    "201": "Created",
    "202": "Accepted",
    "203": "Non-Authoritative Information",
    "204": "No Content",
    "205": "Reset Content",
    "206": "Partial Content",
    "207": "Multi-Status",
    "208": "Already Reported",
    "226": "IM Used",
    "300": "Multiple Choices",
    "301": "Moved Permanently",
    "302": "Found",
    "303": "See Other",
    "304": "Not Modified",
    "305": "Use Proxy",
    "306": "Unused",
    "307": "Temporary Redirect",
    "308": "Permanent Redirect",
    "400": "Bad Request",
    "401": "Unauthorized",
    "402": "Payment Required",
    "403": "Forbidden",
    "404": "Not Found",
    "405": "Method Not Allowed",
    "406": "Not Acceptable",
    "407": "Proxy Authentication Required",
    "408": "Request Timeout",
    "409": "Conflict",
    "410": "Gone",
    "411": "Length Required",
    "412": "Precondition Failed",
    "413": "Payload Too Large",
    "414": "URI Too Long",
    "415": "Unsupported Media Type",
    "416": "Range Not Satisfiable",
    "417": "Expectation Failed",
    "418": "I'm a teapot",
    "421": "Misdirected Request",
    "422": "Unprocessable Entity",
    "423": "Locked",
    "424": "Failed Dependency",
    "425": "Too Early",
    "426": "Upgrade Required",
    "428": "Precondition Required",
    "429": "Too Many Requests",
    "431": "Request Header Fields Too Large",
    "451": "Unavailable For Legal Reasons",
    "500": "Internal Server Error",
    "501": "Not Implemented",
    "502": "Bad Gateway",
    "503": "Service Unavailable",
    "504": "Gateway Timeout",
    "505": "HTTP Version Not Supported",
    "506": "Variant Also Negotiates",
    "507": "Insufficient Storage",
    "508": "Loop Detected",
    "510": "Not Extended",
    "511": "Network Authentication Required",
}

STATUS_TEST_URL = "https://httpbin.org/status/"

print(f"\nConnecting to {ssid}...")
print(f"Signal Strength: {rssi}")
try:
    # Connect to the Wi-Fi network
    wifi.radio.connect(ssid, password)
except OSError as e:
    print(f"❌ OSError: {e}")
print("✅ Wifi!")


print(f" | Status Code Test: {STATUS_TEST_URL}")
# Some return errors then confirm the error (that's a good thing)
# Demonstrates not all errors have the same behavior
# Some 300 level responses contain redirects that requests automatically follows
# By default the response object will contain the status code from the final
# response after all redirect, so it can differ from the expected status code.
for current_code in sorted(http_status_codes.keys(), key=int):
    header_status_test_url = STATUS_TEST_URL + current_code
    with requests.get(header_status_test_url) as response:
        response_status_code = str(response.status_code)
        SORT_STATUS_DESC = http_status_codes.get(
            response_status_code, "Unknown Status Code"
        )
        print_http_status(current_code, response_status_code, SORT_STATUS_DESC)

    # Rate limit ourselves a little to avoid strain on server
    time.sleep(0.5)
print("Finished!")
