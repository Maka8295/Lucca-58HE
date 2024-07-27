# SPDX-FileCopyrightText: 2024 Tyeth Gundry for Adafruit Industries
# SPDX-License-Identifier: MIT

# adafruit_circuitpython_adafruitio usage for batch data with a CPython socket.
import datetime
import socket
import ssl
from random import randint
import adafruit_requests
from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError

# Add a secrets.py to your filesystem that has a dictionary called secrets with "aio_username"
# and "aio_key" entries with your IO credentials, or set environment variables/defaults below.
# *** DO NOT share that file or commit it into Git or other source control. ***
# pylint: disable=no-name-in-module,wrong-import-order
try:
    from secrets import secrets
except ImportError:
    import os

    secrets = {
        "aio_username": os.getenv("ADAFRUIT_AIO_USERNAME", "Your_Username_Here"),
        "aio_key": os.getenv("ADAFRUIT_AIO_KEY", "Your_Adafruit_IO_Key_Here"),
    }
    if (
        secrets["aio_key"] == "Your_Adafruit_IO_Key_Here"
        or secrets["aio_username"] == "Your_Username_Here"
    ):
        print("Adafruit IO secrets are kept in secrets.py, please add them there!")
        raise

# Set your Adafruit IO Username and Key in secrets.py
# (visit io.adafruit.com if you need to create an account,
# or if you need your Adafruit IO key.)
aio_username = secrets["aio_username"]
aio_key = secrets["aio_key"]


requests = adafruit_requests.Session(socket, ssl.create_default_context())
# Initialize an Adafruit IO HTTP API object
io = IO_HTTP(aio_username, aio_key, requests)

try:
    # Get the 'temperature' feed from Adafruit IO
    temperature_feed = io.get_feed("batch-temperature")
except AdafruitIO_RequestError:
    # If no 'temperature' feed exists, create one
    temperature_feed = io.create_new_feed("batch-temperature")

# Get current time from Adafruit IO time service (in UTC)
years, months, days, hours, minutes, seconds, *_ = io.receive_time("UTC")
current_time = datetime.datetime(years, months, days, hours, minutes, seconds)
print("Current time from Adafruit IO: ", current_time)

# Create random values at different timestamps to send to the feed
data = []
for i in range(5):
    random_value = randint(0, 50)
    time_offset = i - 5
    created_at = current_time + datetime.timedelta(seconds=time_offset)
    print(
        "Adding datapoint {0} (at T:{1}) to collection for batch-temperature feed...".format(
            random_value, time_offset
        )
    )
    data.append(
        {
            "value": random_value,
            "created_at": created_at.isoformat(),  # optional metadata like lat, lon, ele, etc
        }
    )

# Send the data to the feed as a single batch
io.send_batch_data(temperature_feed["key"], data)
print("Data sent!")
print()
print(
    "View your feed graph at: https://io.adafruit.com/{0}/feeds/{1}".format(
        aio_username, temperature_feed["key"]
    )
)
print()

# Retrieve data value from the feed
print("Retrieving data from batch-temperature feed...")
received_data = io.receive_data(temperature_feed["key"])
print("Data from temperature feed: ", received_data["value"])
