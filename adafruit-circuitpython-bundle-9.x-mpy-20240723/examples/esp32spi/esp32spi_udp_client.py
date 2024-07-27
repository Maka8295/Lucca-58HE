# SPDX-FileCopyrightText: 2021 Adafruit Industries
# SPDX-License-Identifier: MIT

import struct
import time
from os import getenv
import board
import busio
from digitalio import DigitalInOut
from adafruit_esp32spi import adafruit_esp32spi
import adafruit_esp32spi.adafruit_esp32spi_socketpool as socketpool

# Get wifi details and more from a settings.toml file
# tokens used by this Demo: CIRCUITPY_WIFI_SSID, CIRCUITPY_WIFI_PASSWORD
secrets = {
    "ssid": getenv("CIRCUITPY_WIFI_SSID"),
    "password": getenv("CIRCUITPY_WIFI_PASSWORD"),
}
if secrets == {"ssid": None, "password": None}:
    try:
        # Fallback on secrets.py until depreciation is over and option is removed
        from secrets import secrets  # pylint: disable=no-name-in-module
    except ImportError:
        print("WiFi secrets are kept in settings.toml, please add them there!")
        raise

TIMEOUT = 5
# edit host and port to match server
HOST = "pool.ntp.org"
PORT = 123
NTP_TO_UNIX_EPOCH = 2208988800  # 1970-01-01 00:00:00

# Secondary (SCK1) SPI used to connect to WiFi board on Arduino Nano Connect RP2040
if "SCK1" in dir(board):
    spi = busio.SPI(board.SCK1, board.MOSI1, board.MISO1)
else:
    if "SPI" in dir(board):
        spi = board.SPI()
    else:
        spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
# PyPortal or similar; edit pins as needed
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

# connect to wifi AP
esp.connect(secrets)

# test for connectivity to server
print("Server ping:", esp.ping(HOST), "ms")

# create the socket
pool = socketpool.SocketPool(esp)
socketaddr = pool.getaddrinfo(HOST, PORT)[0][4]
s = pool.socket(type=pool.SOCK_DGRAM)

s.settimeout(TIMEOUT)

print("Sending")
s.connect(socketaddr, conntype=esp.UDP_MODE)
packet = bytearray(48)
packet[0] = 0b00100011  # Not leap second, NTP version 4, Client mode
s.send(packet)

print("Receiving")
packet = s.recv(48)
seconds = struct.unpack_from("!I", packet, offset=len(packet) - 8)[0]
print("Time:", time.localtime(seconds - NTP_TO_UNIX_EPOCH))
