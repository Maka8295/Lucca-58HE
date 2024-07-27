# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-FileCopyrightText: 2021 Adam Cummick
#
# SPDX-License-Identifier: MIT

import board
import busio
import digitalio
from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K
import adafruit_wiznet5k.adafruit_wiznet5k_socketpool as socketpool

print("Wiznet5k SimpleServer Test")

# For Adafruit Ethernet FeatherWing
cs = digitalio.DigitalInOut(board.D10)
# For Particle Ethernet FeatherWing
# cs = digitalio.DigitalInOut(board.D5)
spi_bus = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialize ethernet interface
eth = WIZNET5K(spi_bus, cs, is_dhcp=True)

# Initialize a socket for our server
pool = socketpool.SocketPool(eth)
server = pool.socket()  # Allocate socket for the server
server_ip = eth.pretty_ip(eth.ip_address)  # IP address of server
server_port = 50007  # Port to listen on
server.bind((server_ip, server_port))  # Bind to IP and Port
server.listen()  # Begin listening for incoming clients

while True:
    print(f"Accepting connections on {server_ip}:{server_port}")
    conn, addr = server.accept()  # Wait for a connection from a client.
    print(f"Connection accepted from {addr}, reading exactly 1024 bytes from client")
    with conn:
        data = conn.recv(1024)
        if data:  # Wait for receiving data
            print(data)
            conn.send(data)  # Echo message back to client
    print("Connection closed")
