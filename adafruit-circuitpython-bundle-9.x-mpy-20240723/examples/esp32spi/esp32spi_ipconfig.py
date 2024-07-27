# SPDX-FileCopyrightText: 2019 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
from os import getenv
import board
import busio
from digitalio import DigitalInOut
import adafruit_esp32spi.adafruit_esp32spi_socketpool as socketpool
from adafruit_esp32spi import adafruit_esp32spi

# Get wifi details and more from a settings.toml file
# tokens used by this Demo: CIRCUITPY_WIFI_SSID, CIRCUITPY_WIFI_PASSWORD
secrets = {
    "ssid": getenv("CIRCUITPY_WIFI_SSID"),
    "password": getenv("CIRCUITPY_WIFI_PASSWORD"),
}
if secrets == {"ssid": None, "password": None}:
    try:
        # Fallback on secrets.py until depreciation is over and option is removed
        from secrets import secrets
    except ImportError:
        print("WiFi secrets are kept in settings.toml, please add them there!")
        raise

HOSTNAME = "esp32-spi-hostname-test"

IP_ADDRESS = "192.168.1.111"
GATEWAY_ADDRESS = "192.168.1.1"
SUBNET_MASK = "255.255.255.0"

UDP_IN_ADDR = "192.168.1.1"
UDP_IN_PORT = 5500

UDP_TIMEOUT = 20

# If you are using a board with pre-defined ESP32 Pins:
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)

# If you have an externally connected ESP32:
# esp32_cs = DigitalInOut(board.D9)
# esp32_ready = DigitalInOut(board.D10)
# esp32_reset = DigitalInOut(board.D5)

# Secondary (SCK1) SPI used to connect to WiFi board on Arduino Nano Connect RP2040
if "SCK1" in dir(board):
    spi = busio.SPI(board.SCK1, board.MOSI1, board.MISO1)
else:
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
pool = socketpool.SocketPool(esp)

s_in = pool.socket(type=pool.SOCK_DGRAM)
s_in.settimeout(UDP_TIMEOUT)
print("set hostname:", HOSTNAME)
esp.set_hostname(HOSTNAME)

if esp.status == adafruit_esp32spi.WL_IDLE_STATUS:
    print("ESP32 found and in idle mode")
print("Firmware vers.", esp.firmware_version)
print("MAC addr:", [hex(i) for i in esp.MAC_address])

print("Connecting to AP...")
while not esp.is_connected:
    try:
        esp.connect_AP(secrets["ssid"], secrets["password"])
    except OSError as e:
        print("could not connect to AP, retrying: ", e)
        continue
print("Connected to", esp.ap_info.ssid, "\tRSSI:", esp.ap_info.rssi)
ip1 = esp.ip_address

print("set ip dns")
esp.set_dns_config("192.168.1.1", "8.8.8.8")

print("set ip config")
esp.set_ip_config(IP_ADDRESS, GATEWAY_ADDRESS, SUBNET_MASK)

time.sleep(1)
ip2 = esp.ip_address

time.sleep(1)
info = esp.network_data
print(
    "get network_data: ",
    esp.pretty_ip(info["ip_addr"]),
    esp.pretty_ip(info["gateway"]),
    esp.pretty_ip(info["netmask"]),
)

print("My IP address is", esp.ipv4_address)
print("udp in addr: ", UDP_IN_ADDR, UDP_IN_PORT)

socketaddr_udp_in = pool.getaddrinfo(UDP_IN_ADDR, UDP_IN_PORT)[0][4]
s_in.connect(socketaddr_udp_in, conntype=esp.UDP_MODE)
print("connected local UDP")

while True:
    data = s_in.recv(1205)
    if len(data) >= 1:
        data = data.decode("utf-8")
        print(len(data), data)
