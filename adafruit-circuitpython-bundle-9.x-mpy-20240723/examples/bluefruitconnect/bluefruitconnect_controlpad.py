# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Basic structure example for using the BLE Connect Control Pad
# To use, start this program, and start the Adafruit Bluefruit LE Connect app.
# Connect, and then select Controller-> Control Pad.

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.packet import Packet

# Only the packet classes that are imported will be known to Packet.
from adafruit_bluefruit_connect.button_packet import ButtonPacket

ble = BLERadio()
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)

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
    while ble.connected:
        # Keeping trying until a good packet is received
        try:
            packet = Packet.from_stream(uart_server)
        except ValueError:
            continue

        # Only handle button packets
        if isinstance(packet, ButtonPacket) and packet.pressed:
            if packet.button == ButtonPacket.UP:
                print("Button UP")
            if packet.button == ButtonPacket.DOWN:
                print("Button DOWN")
            if packet.button == ButtonPacket.LEFT:
                print("Button LEFT")
            if packet.button == ButtonPacket.RIGHT:
                print("Button RIGHT")
            if packet.button == ButtonPacket.BUTTON_1:
                print("Button 1")
            if packet.button == ButtonPacket.BUTTON_2:
                print("Button 2")
            if packet.button == ButtonPacket.BUTTON_3:
                print("Button 3")
            if packet.button == ButtonPacket.BUTTON_4:
                print("Button 4")

    # Disconnected
    print("DISCONNECTED")
