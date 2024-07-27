# SPDX-FileCopyrightText: Copyright (c) 2022 Alec Delaney for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import ssl
import wifi
import socketpool
import adafruit_requests as requests
from adafruit_pastebin.pastebin import PasteBin, ExpirationSetting, PrivacySetting

try:
    from secrets import secrets
except ImportError:
    print("Please place your auth/dev key in a secrets.py file!")
    raise

wifi.radio.connect(secrets["ssid"], secrets["password"])
pool = socketpool.SocketPool(wifi.radio)
session = requests.Session(pool, ssl.create_default_context())

auth_key = secrets["auth_key"]

pastebin = PasteBin(session, auth_key)
paste_url = pastebin.paste(
    "This is a test paste!",
    name="My Test Paste",
    expiration=ExpirationSetting.ONE_DAY,
    privacy=PrivacySetting.UNLISTED,
)
print(paste_url)
