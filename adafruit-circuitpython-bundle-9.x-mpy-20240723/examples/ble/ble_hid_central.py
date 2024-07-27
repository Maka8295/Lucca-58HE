# SPDX-FileCopyrightText: 2020 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Demonstration of a Bluefruit BLE Central. Connects to the first BLE HID peripheral it finds.
"""

# import time

# import board

# import adafruit_ble
# from adafruit_ble.services.standard.hid import HIDService
# from adafruit_ble.core.scanner import Scanner

# # This hasn't been updated.

# adafruit_ble.detect_service(HIDService)

# scanner = Scanner()

# while True:
#     print("scanning")
#     results = []
#     while not results:
#         results = scanner.scan(HIDService, timeout=4)

#     peer = results[0].connect(timeout=10, pair=True)
#     print(peer)
#     print(peer.hid.protocol_mode)
#     print(peer.hid.report_map)
#     print(peer.hid.devices)

#     time.sleep(0.2)
