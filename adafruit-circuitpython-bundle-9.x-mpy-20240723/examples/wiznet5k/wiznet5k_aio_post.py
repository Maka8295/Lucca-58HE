# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
from digitalio import DigitalInOut
import adafruit_connection_manager
import adafruit_requests
from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K

# Get Adafruit.io details from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

cs = DigitalInOut(board.D10)
spi_bus = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialize ethernet interface with DHCP
eth = WIZNET5K(spi_bus, cs)
# Initialize a requests session
pool = adafruit_connection_manager.get_radio_socketpool(eth)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(eth)
requests = adafruit_requests.Session(pool, ssl_context)

counter = 0

while True:
    print("Posting data...", end="")
    data = counter
    feed = "test"
    payload = {"value": data}
    response = requests.post(
        "http://io.adafruit.com/api/v2/"
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
    response = None
    time.sleep(15)
