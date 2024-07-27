# SPDX-FileCopyrightText: 2021 Tim C for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
imageload example for esp32s2 that loads an image fetched via
adafruit_requests using BytesIO
"""
from io import BytesIO
import ssl
import wifi
import socketpool

import board
import displayio
import adafruit_requests as requests
import adafruit_imageload

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

wifi.radio.connect(secrets["ssid"], secrets["password"])

print("My IP address is", wifi.radio.ipv4_address)

socket = socketpool.SocketPool(wifi.radio)
https = requests.Session(socket, ssl.create_default_context())

# pylint: disable=line-too-long
url = "https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_ImageLoad/main/examples/images/4bit.bmp"

print("Fetching text from %s" % url)
response = https.get(url)
print("GET complete")

bytes_img = BytesIO(response.content)
image, palette = adafruit_imageload.load(bytes_img)
tile_grid = displayio.TileGrid(image, pixel_shader=palette)

group = displayio.Group(scale=1)
group.append(tile_grid)
board.DISPLAY.root_group = group

response.close()

while True:
    pass
