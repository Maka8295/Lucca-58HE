# SPDX-FileCopyrightText: 2019 Limor Fried for Adafruit Industries
# SPDX-FileCopyrightText: 2023 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
from adafruit_qualia import Qualia
from adafruit_qualia.graphics import Displays

# Set up where we'll be fetching data from
DATA_SOURCE = "https://www.adafruit.com/api/quotes.php"
QUOTE_LOCATION = [0, "text"]
AUTHOR_LOCATION = [0, "author"]

qualia = Qualia(
    Displays.SQUARE34,
    url=DATA_SOURCE,
    json_path=(QUOTE_LOCATION, AUTHOR_LOCATION),
    default_bg=0x333333,
)

qualia.add_text(
    text_position=(20, 120),  # quote location
    text_color=0xFFFFFF,  # quote text color
    text_wrap=25,  # characters to wrap for quote
    text_maxlen=180,  # max text size for quote
    text_scale=3,  # quote text size
)

qualia.add_text(
    text_position=(5, 240),  # author location
    text_color=0x8080FF,  # author text color
    text_wrap=0,  # no wrap for author
    text_maxlen=180,  # max text size for quote & author
    text_scale=3,  # author text size
)

while True:
    try:
        value = qualia.fetch()
        print("Response is", value)
    except (ValueError, RuntimeError, ConnectionError, OSError) as e:
        print("Some error occured, retrying! -", e)
    time.sleep(60)
