# SPDX-FileCopyrightText: 2020 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Used with ble_uart_echo_test.py. Transmits "echo" to the UARTService and receives it back.
"""

import sys

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import (
    ProvideServicesAdvertisement,
    Advertisement,
)
import adafruit_ble_file_transfer

# Connect to a file transfer device
ble = BLERadio()
connection = None
print("disconnected, scanning")
for advertisement in ble.start_scan(
    ProvideServicesAdvertisement, Advertisement, timeout=1
):
    # print(advertisement.address, advertisement.address.type)
    if (
        not hasattr(advertisement, "services")
        or adafruit_ble_file_transfer.FileTransferService not in advertisement.services
    ):
        continue
    connection = ble.connect(advertisement)
    peer_address = advertisement.address
    print("connected to", advertisement.address)
    break
ble.stop_scan()

if not connection:
    print("No advertisement found")
    sys.exit(1)

# Prep the connection
if adafruit_ble_file_transfer.FileTransferService not in connection:
    print("Connected device missing file transfer service")
    sys.exit(1)
if not connection.paired:
    print("pairing")
    connection.pair()
print("paired")
print()
service = connection[adafruit_ble_file_transfer.FileTransferService]
client = adafruit_ble_file_transfer.FileTransferClient(service)

# Do the file operations
print(client.listdir("/"))
print(client.listdir("/lib/"))
