# SPDX-FileCopyrightText: 2024 Justin Myers for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import os

import adafruit_requests
import wifi

import adafruit_connection_manager

TEXT_URL = "http://wifitest.adafruit.com/testwifi/index.html"

wifi_ssid = os.getenv("CIRCUITPY_WIFI_SSID")
wifi_password = os.getenv("CIRCUITPY_WIFI_PASSWORD")

radio = wifi.radio
while not radio.connected:
    radio.connect(wifi_ssid, wifi_password)

# get the pool and ssl_context from the helpers:
pool = adafruit_connection_manager.get_radio_socketpool(radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(radio)

# get request session
requests = adafruit_requests.Session(pool, ssl_context)
connection_manager = adafruit_connection_manager.get_connection_manager(pool)
print("-" * 40)
print("Nothing yet opened")
print(f"Managed Sockets: {connection_manager.managed_socket_count}")
print(f"Available Managed Sockets: {connection_manager.available_socket_count}")

# make request
print("-" * 40)
print(f"Fetching from {TEXT_URL} in a context handler")
with requests.get(TEXT_URL) as response:
    response_text = response.text
    print(f"Text Response {response_text}")

print("-" * 40)
print("1 request, opened and closed")
print(f"Managed Sockets: {connection_manager.managed_socket_count}")
print(f"Available Managed Sockets: {connection_manager.available_socket_count}")

print("-" * 40)
print(f"Fetching from {TEXT_URL} not in a context handler")
response = requests.get(TEXT_URL)

print("-" * 40)
print("1 request, opened but not closed")
print(f"Managed Sockets: {connection_manager.managed_socket_count}")
print(f"Available Managed Sockets: {connection_manager.available_socket_count}")

print("-" * 40)
print("Closing everything in the pool")
adafruit_connection_manager.connection_manager_close_all(pool)

print("-" * 40)
print("Everything closed")
print(f"Managed Sockets: {connection_manager.managed_socket_count}")
print(f"Available Managed Sockets: {connection_manager.available_socket_count}")
