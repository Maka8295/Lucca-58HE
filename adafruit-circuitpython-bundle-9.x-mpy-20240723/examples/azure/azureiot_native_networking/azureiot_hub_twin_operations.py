# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import random
import time

import rtc
import wifi

import adafruit_connection_manager
import adafruit_ntp
from adafruit_azureiot import IoTHubDevice

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

# You will need an Azure subscription to create an Azure IoT Hub resource
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
# Create an Azure IoT Hub and an IoT device in the Azure portal here:
# https://aka.ms/AzurePortalHome.
# Instructions to create an IoT Hub and device are here: https://aka.ms/CreateIoTHub
#
# The free tier of IoT Hub allows up to 8,000 messages a day, so try not to send messages too often
# if you are using the free tier
#
# Once you have a hub and a device, copy the device primary connection string.
# Add it to the secrets.py file in an entry called device_connection_string
#
# The adafruit-circuitpython-azureiot library depends on the following libraries:
#
# From the Adafruit CircuitPython Bundle https://github.com/adafruit/Adafruit_CircuitPython_Bundle:
# * adafruit-circuitpython-minimqtt


# Create an IoT Hub device client and connect
device = IoTHubDevice(pool, ssl_context, secrets["device_connection_string"])


# Subscribe to device twin desired property updates
# To see these changes, update the desired properties for the device either in code
# or in the Azure portal by selecting the device in the IoT Hub blade, selecting
# Device Twin then adding or amending an entry in the 'desired' section
def device_twin_desired_updated(
    desired_property_name: str, desired_property_value, desired_version: int
):
    print(
        "Property",
        desired_property_name,
        "updated to",
        str(desired_property_value),
        "version",
        desired_version,
    )


# Subscribe to the device twin desired property updated event
device.on_device_twin_desired_updated = device_twin_desired_updated

print("Connecting to Azure IoT Hub...")
device.connect()

print("Connected to Azure IoT Hub!")

message_counter = 60

while True:
    try:
        if message_counter >= 60:
            # Send a reported property twin update every minute
            # You can see these in the portal by selecting the device in the IoT Hub blade,
            # selecting device Twin then looking for the updates in the 'reported' section
            patch = {"Temperature": random.randint(0, 50)}
            device.update_twin(patch)
            message_counter = 0
        else:
            message_counter += 1

        # Poll every second for messages from the cloud
        device.loop()
    except (ValueError, RuntimeError) as e:
        print("Connection error, reconnecting\n", str(e))
        # If we lose connectivity, reset the wifi and reconnect
        wifi.radio.enabled = False
        wifi.radio.enabled = True
        wifi.radio.connect(secrets["ssid"], secrets["password"])
        device.reconnect()
        continue
    time.sleep(1)
