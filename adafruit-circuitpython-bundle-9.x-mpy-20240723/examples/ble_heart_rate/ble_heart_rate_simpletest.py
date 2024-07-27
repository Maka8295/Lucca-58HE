# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Read heart rate data from a heart rate peripheral using the standard BLE
Heart Rate service.
"""

import time

import adafruit_ble
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.device_info import DeviceInfoService
from adafruit_ble_heart_rate import HeartRateService

# PyLint can't find BLERadio for some reason so special case it here.
ble = adafruit_ble.BLERadio()  # pylint: disable=no-member

hr_connection = None

while True:
    print("Scanning...")
    for adv in ble.start_scan(ProvideServicesAdvertisement, timeout=5):
        if HeartRateService in adv.services:
            print("found a HeartRateService advertisement")
            hr_connection = ble.connect(adv)
            print("Connected")
            break

    # Stop scanning whether or not we are connected.
    ble.stop_scan()
    print("Stopped scan")

    if hr_connection and hr_connection.connected:
        print("Fetch connection")
        if DeviceInfoService in hr_connection:
            dis = hr_connection[DeviceInfoService]
            try:
                manufacturer = dis.manufacturer
            except AttributeError:
                manufacturer = "(Manufacturer Not specified)"
            try:
                model_number = dis.model_number
            except AttributeError:
                model_number = "(Model number not specified)"
            print("Device:", manufacturer, model_number)
        else:
            print("No device information")
        hr_service = hr_connection[HeartRateService]
        print("Location:", hr_service.location)
        while hr_connection.connected:
            print(hr_service.measurement_values)
            time.sleep(1)
