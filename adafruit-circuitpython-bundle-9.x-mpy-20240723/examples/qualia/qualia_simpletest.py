# SPDX-FileCopyrightText: 2023 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
#
# NOTE: Make sure you've set up your settings.toml file before running this example
# https://learn.adafruit.com/getting-started-with-web-workflow-using-the-code-editor/

from adafruit_qualia import Qualia
from adafruit_qualia.graphics import Displays

# Set a data source URL
TEXT_URL = "http://wifitest.adafruit.com/testwifi/index.html"

# Create the Qualia object
qualia = Qualia(Displays.SQUARE34, url=TEXT_URL)

# Go get that data
print("Fetching text from", TEXT_URL)
data = qualia.fetch()

# Print out what we got
print("-" * 40)
print(data)
print("-" * 40)
