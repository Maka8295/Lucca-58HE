# SPDX-FileCopyrightText: Copyright (c) 2022 Alec Delaney for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import ssl
import socket
import adafruit_requests as requests
from adafruit_pastebin.adafruit_io import AIOPastebin

try:
    from secrets import secrets
except ImportError:
    print("Please place your auth/dev key in a secrets.py file!")
    raise

auth_key = secrets["auth_key"]

session = requests.Session(socket, ssl_context=ssl.create_default_context())

pastebin = AIOPastebin(
    session, auth_key, username="username", feed_key="existing_feedkey"
)
paste_url = pastebin.paste(
    "This is a test paste!",
)
print(paste_url)
