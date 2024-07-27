# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Basic structure example for using the BLE Connect Controller sensors
# To use, start this program, and start the Adafruit Bluefruit LE Connect app.
# Connect, and then select Controller and enable the sensors

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.packet import Packet

# Only the packet classes that are imported will be known to Packet.
from adafruit_bluefruit_connect.accelerometer_packet import AccelerometerPacket
from adafruit_bluefruit_connect.gyro_packet import GyroPacket
from adafruit_bluefruit_connect.location_packet import LocationPacket
from adafruit_bluefruit_connect.magnetometer_packet import MagnetometerPacket
from adafruit_bluefruit_connect.quaternion_packet import QuaternionPacket

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

        # Accelerometer
        if isinstance(packet, AccelerometerPacket):
            print("Accelerometer:", packet.x, packet.y, packet.z)

        # Gyro
        if isinstance(packet, GyroPacket):
            print("Gyro:", packet.x, packet.y, packet.z)

        # Location
        if isinstance(packet, LocationPacket):
            print("Location:", packet.latitude, packet.longitude, packet.altitude)

        # Magnetometer
        if isinstance(packet, MagnetometerPacket):
            print("Magnetometer", packet.x, packet.y, packet.z)

        # Quaternion
        if isinstance(packet, QuaternionPacket):
            print("Quaternion:", packet.x, packet.y, packet.z, packet.w)

    # Disconnected
    print("DISCONNECTED")
