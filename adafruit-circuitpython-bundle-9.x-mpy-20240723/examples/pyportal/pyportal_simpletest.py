# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# NOTE: Make sure you've created your secrets.py file before running this example
# https://learn.adafruit.com/adafruit-pyportal/internet-connect#whats-a-secrets-file-17-2
import board
from displayio import CIRCUITPYTHON_TERMINAL
from adafruit_pyportal import PyPortal


# Set a data source URL
TEXT_URL = "http://wifitest.adafruit.com/testwifi/index.html"

# Create the PyPortal object
pyportal = PyPortal(url=TEXT_URL, status_neopixel=board.NEOPIXEL)

# Set display to show REPL
board.DISPLAY.root_group = CIRCUITPYTHON_TERMINAL

# Go get that data
print("Fetching text from", TEXT_URL)
data = pyportal.fetch()

# Print out what we got
print("-" * 40)
print(data)
print("-" * 40)
