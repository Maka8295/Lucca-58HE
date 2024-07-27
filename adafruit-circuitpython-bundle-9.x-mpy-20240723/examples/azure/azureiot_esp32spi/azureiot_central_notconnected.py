# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import json
import random
import time
import board
import busio
from digitalio import DigitalInOut
import neopixel
import rtc
from adafruit_esp32spi import adafruit_esp32spi, adafruit_esp32spi_wifimanager
import adafruit_connection_manager

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# ESP32 Setup
try:
    esp32_cs = DigitalInOut(board.ESP_CS)
    esp32_ready = DigitalInOut(board.ESP_BUSY)
    esp32_reset = DigitalInOut(board.ESP_RESET)
except AttributeError:
    esp32_cs = DigitalInOut(board.D13)
    esp32_ready = DigitalInOut(board.D11)
    esp32_reset = DigitalInOut(board.D12)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

"""Use below for Most Boards"""
status_light = neopixel.NeoPixel(
    board.NEOPIXEL, 1, brightness=0.2
)  # Uncomment for Most Boards
"""Uncomment below for ItsyBitsy M4"""
# status_light = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)
# Uncomment below for an externally defined RGB LED
# import adafruit_rgbled
# from adafruit_esp32spi import PWMOut
# RED_LED = PWMOut.PWMOut(esp, 26)
# GREEN_LED = PWMOut.PWMOut(esp, 27)
# BLUE_LED = PWMOut.PWMOut(esp, 25)
# status_light = adafruit_rgbled.RGBLED(RED_LED, BLUE_LED, GREEN_LED)
wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets, status_light)

print("Connecting to WiFi...")

wifi.connect()

print("Connected to WiFi!")

print("Getting the time...")

rtc.RTC().datetime = time.localtime(esp.get_time()[0])

print("Time:", str(time.time()))

# To use Azure IoT Central, you will need to create an IoT Central app.
# You can either create a free tier app that will live for 7 days without an Azure subscription,
# Or a standard tier app that will last for ever with an Azure subscription.
# The standard tiers are free for up to 2 devices
#
# If you don't have an Azure subscription:
#
# If you are a student, head to https://aka.ms/FreeStudentAzure and sign up, validating with your
#  student email address. This will give you $100 of Azure credit and free tiers of a load of
#  service, renewable each year you are a student
#
# If you are not a student, head to https://aka.ms/FreeAz and sign up to get $200 of credit for 30
#  days, as well as free tiers of a load of services
#
# Create an Azure IoT Central app by following these instructions:
# https://aka.ms/CreateIoTCentralApp
# Add a device template with telemetry, properties and commands, as well as a view to visualize the
# telemetry and execute commands, and a form to set properties.
#
# Next create a device using the device template, and select Connect to get the device connection
# details.
# Add the connection details to your secrets.py file, using the following values:
#
# 'id_scope' - the devices ID scope
# 'device_id' - the devices device id
# 'device_sas_key' - the devices primary key
#
# The adafruit-circuitpython-azureiot library depends on the following libraries:
#
# From the Adafruit CircuitPython Bundle https://github.com/adafruit/Adafruit_CircuitPython_Bundle:
# * adafruit-circuitpython-minimqtt
# pylint: disable=wrong-import-position
from adafruit_azureiot import (
    IoTCentralDevice,
    IoTError,
)

# pylint: enable=wrong-import-position

pool = adafruit_connection_manager.get_radio_socketpool(esp)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(esp)
# Create an IoT Hub device client and connect
device = IoTCentralDevice(
    pool,
    ssl_context,
    secrets["id_scope"],
    secrets["device_id"],
    secrets["device_sas_key"],
)

# don't connect
# device.connect()

try:
    message = {"Temperature": random.randint(0, 50)}
    device.send_telemetry(json.dumps(message))
except IoTError as iot_error:
    print("Error - ", iot_error.message)
