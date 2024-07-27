# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# pylint: disable=unused-import
import time
import board
import busio
import digitalio
from adafruit_fona.adafruit_fona import FONA, FONA_3G_A, FONA_3G_E
from adafruit_fona.fona_3g import FONA3G

print("FONA SMS")

# Create a serial connection for the FONA connection
uart = busio.UART(board.TX, board.RX)
rst = digitalio.DigitalInOut(board.D4)

# Use this for FONA800 and FONA808
fona = FONA(uart, rst)

# Use this for FONA3G
# fona = FONA3G(uart, rst)

# Initialize network
while fona.network_status != 1:
    print("Connecting to network...")
    time.sleep(1)
print("Connected to network!")
print("RSSI: %ddB" % fona.rssi)

# Text a number
print("Sending SMS...")
if not fona.send_sms(140404, "HELP"):
    raise RuntimeError("FONA did not successfully send SMS")
print("SMS Sent!")

# Ask the FONA how many SMS message it has stored
num_sms = fona.num_sms()
print("%d SMS's on SIM Card" % num_sms)

# FONA3G SMS memory slots start at 0
if fona.version in (FONA_3G_A, FONA_3G_E):
    sms_idx = 0
else:  # FONA800 and FONA808 SMS slots start at 1
    sms_idx = 1

# Read num_sms messages from the FONA
for slot in range(sms_idx, num_sms):
    print(fona.read_sms(slot))
