# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# pylint: disable=unused-import
import time
import board
import busio
import digitalio
from adafruit_fona.adafruit_fona import FONA
from adafruit_fona.fona_3g import FONA3G

print("FONA SMS Response")

# Create a serial connection for the FONA connection
uart = busio.UART(board.TX, board.RX)
rst = digitalio.DigitalInOut(board.D4)
# Ring Indicator (RI) interrupt pin
ri = digitalio.DigitalInOut(board.D5)

# Use this for FONA800 and FONA808
fona = FONA(uart, rst, ri)

# Use this for FONA3G
# fona = FONA3G(uart, rst, ri)

# Initialize Network
while fona.network_status != 1:
    print("Connecting to network...")
    time.sleep(1)
print("Connected to network!")
print("RSSI: %ddB" % fona.rssi)

# Enable FONA SMS notification
fona.enable_sms_notification = True

print("FONA Ready!\nWaiting for SMS...")
while True:
    sender, message = fona.receive_sms()

    if message:
        print("Incoming SMS from {}: {}".format(sender, message))

        # Reply back!
        print("Sending response...")
        if not fona.send_sms(int(sender), "Hey, I got your text!"):
            print("SMS Send Failed")
        print("SMS Sent!")
