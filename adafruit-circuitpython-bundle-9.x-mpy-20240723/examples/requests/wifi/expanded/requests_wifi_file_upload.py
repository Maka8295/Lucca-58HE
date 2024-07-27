# SPDX-FileCopyrightText: 2024 Tim Cocks for Adafruit Industries
# SPDX-License-Identifier: MIT

import adafruit_connection_manager
import wifi

import adafruit_requests

URL = "https://httpbin.org/post"

pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)

with open("requests_wifi_file_upload_image.png", "rb") as file_handle:
    files = {
        "file": (
            "requests_wifi_file_upload_image.png",
            file_handle,
            "image/png",
            {"CustomHeader": "BlinkaRocks"},
        ),
        "othervalue": (None, "HelloWorld"),
    }

    with requests.post(URL, files=files) as response:
        print(response.content)
