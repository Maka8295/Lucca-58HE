# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import json
import random
import time

import rtc
import wifi

import adafruit_connection_manager
import adafruit_ntp
from adafruit_azureiot import IoTCentralDevice

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

print("Connecting to WiFi...")
wifi.radio.connect(secrets["ssid"], secrets["password"])

pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)

print("Connected to WiFi!")

if time.localtime().tm_year < 2022:
    print("Setting System Time in UTC")
    ntp = adafruit_ntp.NTP(pool, tz_offset=0)

    # NOTE: This changes the system time so make sure you aren't assuming that time
    # doesn't jump.
    rtc.RTC().datetime = ntp.datetime
else:
    print("Year seems good, skipping set time.")

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


# Create an IoT Hub device client and connect
device = IoTCentralDevice(
    pool,
    ssl_context,
    secrets["id_scope"],
    secrets["device_id"],
    secrets["device_sas_key"],
)

print("Connecting to Azure IoT Central...")
device.connect()

print("Connected to Azure IoT Central!")

message_counter = 60

while True:
    try:
        # Send telemetry every minute
        # You can see the values in the devices dashboard
        if message_counter >= 60:
            message = {"Temperature": random.randint(0, 50)}
            device.send_telemetry(json.dumps(message))
            message_counter = 0
        else:
            message_counter += 1

        # Poll every second for messages from the cloud
        device.loop()
    except (ValueError, RuntimeError) as e:
        print("Connection error, reconnecting\n", str(e))
        wifi.radio.enabled = False
        wifi.radio.enabled = True
        wifi.radio.connect(secrets["ssid"], secrets["password"])
        device.reconnect()
        continue
    time.sleep(1)
