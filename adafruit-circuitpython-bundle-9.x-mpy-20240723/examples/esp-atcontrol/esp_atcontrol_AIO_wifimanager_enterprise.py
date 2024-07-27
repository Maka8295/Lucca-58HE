# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Note, you must create a feed called "test" in your AdafruitIO account.
# Your secrets file must contain your aio_username and aio_key

import time
import board
import busio
from digitalio import DigitalInOut
from digitalio import Direction
import neopixel

# ESP32 AT
from adafruit_espatcontrol import (
    adafruit_espatcontrol,
    adafruit_espatcontrol_wifimanager,
)

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

pixel_status = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.3, auto_write=True)

# Debug Level
# Change the Debug Flag if you have issues with AT commands
debugflag = False

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
    RX = board.TX
    TX = board.RX
    resetpin = DigitalInOut(board.D4)
    rtspin = DigitalInOut(board.D5)
    uart = busio.UART(board.TX, board.RX, timeout=0.1)
    esp_boot = DigitalInOut(board.D9)
    esp_boot.direction = Direction.OUTPUT
    esp_boot.value = True
    status_light = pixel_status

print("ESP AT commands")
esp = adafruit_espatcontrol.ESP_ATcontrol(
    uart, 115200, reset_pin=resetpin, rts_pin=rtspin, debug=debugflag
)
wifi = adafruit_espatcontrol_wifimanager.ESPAT_WiFiManager(
    esp, secrets, status_light, enterprise=True, debug=debugflag
)
wifi.disconnect()
wifi.reset(soft_reset=True)

counter = 0

while True:
    try:
        print("Posting data...", end="")
        data = counter
        feed = "example"
        payload = {"value": data}
        response = wifi.post(
            "https://io.adafruit.com/api/v2/"
            + secrets["aio_username"]
            + "/feeds/"
            + feed
            + "/data",
            json=payload,
            headers={"X-AIO-KEY": secrets["aio_key"]},
        )
        print(response.json())
        response.close()

        counter = counter + 1
        print("OK")
        wifi.disconnect()

    except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
        print("Failed to get data, retrying\n", e)
        wifi.reset(soft_reset=True)
        continue
    response = None
    time.sleep(15)
