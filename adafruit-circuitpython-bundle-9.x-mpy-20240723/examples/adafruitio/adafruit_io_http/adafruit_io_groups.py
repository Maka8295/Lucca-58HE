# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Adafruit IO HTTP API - Group Interactions
# Documentation: https://io.adafruit.com/api/docs/#groups
# adafruit_circuitpython_adafruitio with an esp32spi_socket
import adafruit_datetime as datetime
import board
import busio
from digitalio import DigitalInOut
import adafruit_connection_manager
from adafruit_esp32spi import adafruit_esp32spi
import adafruit_requests
from adafruit_io.adafruit_io import IO_HTTP


# Add a secrets.py to your filesystem that has a dictionary called secrets with "ssid" and
# "password" keys with your WiFi credentials, along with "aio_username" and "aio_key" for
# your Adafruit IO user/key. DO NOT share that file or commit it into Git or other source control.
# pylint: disable=no-name-in-module,wrong-import-order
try:
    from secrets import secrets
except ImportError:
    import os

    if os.getenv("ADAFRUIT_AIO_USERNAME") and os.getenv("ADAFRUIT_AIO_KEY"):
        secrets = {
            "aio_username": os.getenv("ADAFRUIT_AIO_USERNAME", "Your_Username_Here"),
            "aio_key": os.getenv("ADAFRUIT_AIO_KEY", "Your_Adafruit_IO_Key_Here"),
            "ssid": os.getenv("CIRCUITPY_WIFI_SSID", ""),
            "password": os.getenv("CIRCUITPY_WIFI_PASSWORD", ""),
        }
    else:
        print(
            "WiFi + Adafruit IO secrets are kept in secrets.py, please add them there!"
        )
        raise

# If you are using a board with pre-defined ESP32 Pins:
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)

# If you have an externally connected ESP32:
# esp32_cs = DigitalInOut(board.D9)
# esp32_ready = DigitalInOut(board.D10)
# esp32_reset = DigitalInOut(board.D5)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

print("Connecting to AP...")
while not esp.is_connected:
    try:
        esp.connect_AP(secrets["ssid"], secrets["password"])
    except RuntimeError as e:
        print("could not connect to AP, retrying: ", e)
        continue
print("Connected to", str(esp.ssid, "utf-8"), "\tRSSI:", esp.rssi)

# If you are using a wifi based mcu use this instead of esp code above, remove the from
# adafruit_esp32spi import line, optionally esp.connect(secrets["ssid"], secrets["password"])
# import wifi
# esp = wifi.radio

# Initialize a requests session
pool = adafruit_connection_manager.get_radio_socketpool(esp)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(esp)
requests = adafruit_requests.Session(pool, ssl_context)

# If you are testing on python with blinka, use real requests below and comment out above:
# import os, datetime, requests as real_requests
# from adafruit_io.adafruit_io import IO_HTTP
# secrets = {
#     "aio_username": os.getenv("ADAFRUIT_AIO_USERNAME"),
#     "aio_key": os.getenv("ADAFRUIT_AIO_KEY"),
# }
# requests = real_requests.Session()


# Set your Adafruit IO Username and Key in secrets.py
# (visit io.adafruit.com if you need to create an account,
# or if you need your Adafruit IO key.)
aio_username = secrets["aio_username"]
aio_key = secrets["aio_key"]

# Initialize an Adafruit IO HTTP API object
io = IO_HTTP(aio_username, aio_key, requests)

# Create a new group
print("Creating a new Adafruit IO Group...")
sensor_group = io.create_new_group("envsensors", "a group of environmental sensors")

# Create the 'temperature' feed in the group
print("Creating feed temperature inside group...")
io.create_feed_in_group(sensor_group["key"], "temperature")

# Create the 'humidity' feed then add to group (it will still be in Default group too)
print("Creating feed humidity then adding to group...")
humidity_feed = io.create_new_feed("humidity", "a feed for humidity data")
io.add_feed_to_group(sensor_group["key"], humidity_feed["key"])

# show humidity feed is in two groups
print("Getting fresh humidity feed info... (notice groups)")
print(io.get_feed(humidity_feed["key"]))

# fetch current time
print("Fetching current time from IO... ", end="")
year, month, day, hour, minute, second, *_ = io.receive_time(timezone="UTC")
old_time = datetime.datetime(year, month, day, hour, minute, second)
print(old_time.isoformat())

# Publish data for multiple feeds to a group, use different timestamps for no reason
print("Publishing batch data to group feeds with created_at set 99minutes ago...")
thetime = old_time - datetime.timedelta(minutes=99)
print(thetime)

io.send_group_data(
    group_key=sensor_group["key"],
    feeds_and_data=[
        {"key": "temperature", "value": 20.0},
        {"key": "humidity", "value": 40.0},
    ],
    metadata={
        "lat": 50.1858942,
        "lon": -4.9677478,
        "ele": 4,
        "created_at": thetime.isoformat(),
    },
)

# Get info from the group
print("Getting fresh group info... (notice created_at vs updated_at)")
sensor_group = io.get_group("envsensors")  # refresh data via HTTP API
print(sensor_group)

# Delete the group
print("Deleting group...")
io.delete_group("envsensors")

# Delete the remaining humidity feed (it was in Two Groups so not deleted with our group)
print("Deleting feed humidity (still in default group)...")
io.delete_feed(humidity_feed["key"])
