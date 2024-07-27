# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
from digitalio import DigitalInOut
from digitalio import Direction
import rtc

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

# Debug Level
# Change the Debug Flag if you have issues with AT commands
debugflag = False

# How Long to sleep between polling
sleep_duration = 5

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
wifi = adafruit_espatcontrol_wifimanager.ESPAT_WiFiManager(esp, secrets, status_light)


print("ESP32 local time")

TIME_API = "http://worldtimeapi.org/api/ip"


the_rtc = rtc.RTC()

response = None
while True:
    try:
        print("Fetching json from", TIME_API)
        response = wifi.get(TIME_API)
        break
    except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
        print("Failed to get data, retrying\n", e)
        continue

json = response.json()
current_time = json["datetime"]
the_date, the_time = current_time.split("T")
year, month, mday = [int(x) for x in the_date.split("-")]
the_time = the_time.split(".")[0]
hours, minutes, seconds = [int(x) for x in the_time.split(":")]

# We can also fill in these extra nice things
year_day = json["day_of_year"]
week_day = json["day_of_week"]
is_dst = json["dst"]

now = time.struct_time(
    (year, month, mday, hours, minutes, seconds, week_day, year_day, is_dst)
)
print(now)
the_rtc.datetime = now

while True:
    print(time.localtime())
    print("Sleeping for: {0} Seconds".format(sleep_duration))
    time.sleep(sleep_duration)
