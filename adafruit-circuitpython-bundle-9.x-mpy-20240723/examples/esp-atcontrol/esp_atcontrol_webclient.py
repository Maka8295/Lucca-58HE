# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
from digitalio import DigitalInOut
from digitalio import Direction
import adafruit_connection_manager
import adafruit_requests
import adafruit_espatcontrol.adafruit_espatcontrol_socket as pool
from adafruit_espatcontrol import adafruit_espatcontrol


# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# Debug Level
# Change the Debug Flag if you have issues with AT commands
debugflag = False

# How long between queries
TIME_BETWEEN_QUERY = 60  # in seconds

if board.board_id == "challenger_rp2040_wifi":
    RX = board.ESP_RX
    TX = board.ESP_TX
    resetpin = DigitalInOut(board.WIFI_RESET)
    rtspin = False
    uart = busio.UART(TX, RX, baudrate=11520, receiver_buffer_size=2048)
    esp_boot = DigitalInOut(board.WIFI_MODE)
    esp_boot.direction = Direction.OUTPUT
    esp_boot.value = True
    status_light = None
else:
    RX = board.ESP_TX
    TX = board.ESP_RX
    resetpin = DigitalInOut(board.ESP_WIFI_EN)
    rtspin = DigitalInOut(board.ESP_CTS)
    uart = busio.UART(TX, RX, timeout=0.1)
    esp_boot = DigitalInOut(board.ESP_BOOT_MODE)
    esp_boot.direction = Direction.OUTPUT
    esp_boot.value = True
    status_light = None

print("ESP AT commands")
esp = adafruit_espatcontrol.ESP_ATcontrol(
    uart, 115200, reset_pin=resetpin, rts_pin=rtspin, debug=debugflag
)

URL = "http://wifitest.adafruit.com/testwifi/index.html"
print("ESP AT GET URL", URL)

print("Resetting ESP module")
esp.hard_reset()

ssl_context = adafruit_connection_manager.create_fake_ssl_context(pool, esp)
requests = adafruit_requests.Session(pool, ssl_context)

while True:
    try:
        print("Checking connection...")
        while not esp.is_connected:
            print("Connecting...")
            esp.connect(secrets)
        # great, lets get the data
        print("Retrieving URL...", end="")
        r = requests.get(URL)
        print("Status:", r.status_code)
        print("Content type:", r.headers["content-type"])
        print("Content size:", r.headers["content-length"])
        print("Encoding:", r.encoding)
        print("Text:", r.text)
        print("Sleeping for: {0} Seconds".format(TIME_BETWEEN_QUERY))
        time.sleep(TIME_BETWEEN_QUERY)
    except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
        print("Failed to get data, retrying\n", e)
        continue
