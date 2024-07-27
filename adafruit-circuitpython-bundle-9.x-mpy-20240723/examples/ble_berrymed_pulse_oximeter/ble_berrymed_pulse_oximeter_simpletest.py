# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Read data from a BerryMed pulse oximeter, model BM1000C, BM1000E, etc.
"""

# Protocol defined here:
#     https://github.com/zh2x/BCI_Protocol
# Thanks as well to:
#     https://github.com/ehborisov/BerryMed-Pulse-Oximeter-tool
#     https://github.com/ScheindorfHyenetics/berrymedBluetoothOxymeter
#
# The sensor updates the readings at 100Hz.

import _bleio
import adafruit_ble
from adafruit_ble.advertising.standard import Advertisement
from adafruit_ble.services.standard.device_info import DeviceInfoService
from adafruit_ble_berrymed_pulse_oximeter import BerryMedPulseOximeterService

# CircuitPython <6 uses its own ConnectionError type. So, is it if available. Otherwise,
# the built in ConnectionError is used.
connection_error = ConnectionError
if hasattr(_bleio, "ConnectionError"):
    connection_error = _bleio.ConnectionError

# PyLint can't find BLERadio for some reason so special case it here.
ble = adafruit_ble.BLERadio()  # pylint: disable=no-member

pulse_ox_connection = None

while True:
    print("Scanning...")
    for adv in ble.start_scan(Advertisement, timeout=5):
        name = adv.complete_name
        if not name:
            continue
        # "BerryMed" devices may have trailing nulls on their name.
        if name.strip("\x00") == "BerryMed":
            pulse_ox_connection = ble.connect(adv)
            print("Connected")
            break

    # Stop scanning whether or not we are connected.
    ble.stop_scan()
    print("Stopped scan")

    try:
        if pulse_ox_connection and pulse_ox_connection.connected:
            print("Fetch connection")
            if DeviceInfoService in pulse_ox_connection:
                dis = pulse_ox_connection[DeviceInfoService]
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
            pulse_ox_service = pulse_ox_connection[BerryMedPulseOximeterService]
            while pulse_ox_connection.connected:
                print(pulse_ox_service.values)
    except connection_error:
        try:
            pulse_ox_connection.disconnect()
        except connection_error:
            pass
        pulse_ox_connection = None
