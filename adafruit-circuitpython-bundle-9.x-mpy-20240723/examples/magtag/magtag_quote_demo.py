# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import os
from adafruit_magtag.magtag import MagTag

# Set up where we'll be fetching data from
DATA_SOURCE = "https://www.adafruit.com/api/quotes.php"
QUOTE_LOCATION = [0, "text"]
AUTHOR_LOCATION = [0, "author"]

# the current working directory (where this file is)
try:
    cwd = os.path.dirname(os.path.realpath(__file__))
except AttributeError:
    cwd = ("/" + __file__).rsplit("/", 1)[0]

magtag = MagTag(
    url=DATA_SOURCE,
    json_path=(QUOTE_LOCATION, AUTHOR_LOCATION),
    default_bg=0x000000,
)


def add_quote_marks(quote_text):
    return f'"{quote_text}"'


def add_hyphen(author_name):
    return f"- {author_name}"


magtag.add_text(
    text_position=(
        (magtag.graphics.display.width // 2) - 1,
        (magtag.graphics.display.height // 2) - 20,
    ),
    text_color=0xFFFFFF,
    text_wrap=44,
    text_maxlen=180,
    line_spacing=1.0,
    text_transform=add_quote_marks,
    text_anchor_point=(0.5, 0.5),
)

magtag.add_text(
    text_position=(
        (magtag.graphics.display.width // 2) - 120,
        (magtag.graphics.display.height // 2) + 34,
    ),
    text_color=0xFFFFFF,
    text_wrap=0,
    text_maxlen=30,
    text_transform=add_hyphen,
)

try:
    value = magtag.fetch()
    print("Response is", value)
except (ValueError, RuntimeError) as e:
    print("Some error occured, retrying! -", e)
magtag.exit_and_deep_sleep(60)
