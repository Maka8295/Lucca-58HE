# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# This file is where you keep secret settings, passwords, and tokens!
# If you put them in the code you risk committing that info or sharing it
# which would be not great. So, instead, keep it all in this one file and
# keep it a secret.

# To find out how to hide any changes you make to this file from Git, check out
# this blog post: https://www.jimbobbennett.io/hiding-api-keys-from-git/

"""
Contains the secrets for your app including WiFi connection details.
DO NOT CHECK THIS INTO SOURCE CODE CONTROL!!!!11!!!
"""

secrets = {
    # WiFi settings
    "ssid": "",
    "password": "",
    # Azure IoT Central settings - if you are connecting to Azure IoT Central, fill in these three
    # values
    # To get these values, select your device in Azure IoT Central,
    # then select the Connect button
    # A dialog will appear with these three values
    # id_scope comes from the ID scope value
    # device_id comes from the Device ID value
    # key comes from either the Primary key or Secondary key
    "id_scope": "",
    "device_id": "",
    "device_sas_key": "",
    # Azure IoT Hub settings - if you are connecting to Azure IoT Hub, fill in this value
    # To get this value, from the Azure Portal (https://aka.ms/AzurePortalHome), select your IoT
    # Hub, then select Explorers -> IoT devices, select your device, then copy the entire primary
    # or secondary connection string using the copy button next to the value and set this here.
    # It will be in the format:
    #   HostName=<your-hub>.azure-devices.net;DeviceId=<your device id>;SharedAccessKey=<key>
    # Note - you need the primary or secondary connection string, NOT the primary or secondary key
    "device_connection_string": "",
}
