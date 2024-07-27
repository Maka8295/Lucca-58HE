# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Basic example for using the BLE Connect UART
# To use, start this program, and start the Adafruit Bluefruit LE Connect app.
# Connect, and then select UART. Any text received FROM the connected device
# will be displayed. Periodically, text is sent TO the connected device.

import time
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

SEND_RATE = 10  # how often in seconds to send text

ble = BLERadio()
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)

count = 0
while True:
    print("WAITING...")
    # Advertise when not connected.
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass

    # Connected
    ble.stop_advertising()
    print("CONNECTED")

    # Loop and read packets
    last_send = time.monotonic()
    while ble.connected:
        # INCOMING (RX) check for incoming text
        if uart_server.in_waiting:
            raw_bytes = uart_server.read(uart_server.in_waiting)
            text = raw_bytes.decode().strip()
            # print("raw bytes =", raw_bytes)
            print("RX:", text)
        # OUTGOING (TX) periodically send text
        if time.monotonic() - last_send > SEND_RATE:
            text = "COUNT = {}\r\n".format(count)
            print("TX:", text.strip())
            uart_server.write(text.encode())
            count += 1
            last_send = time.monotonic()

    # Disconnected
    print("DISCONNECTED")
