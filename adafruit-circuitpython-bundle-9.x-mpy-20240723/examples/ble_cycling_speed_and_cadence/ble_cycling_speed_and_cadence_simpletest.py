# SPDX-FileCopyrightText: 2020 Dan Halbert for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Read cycling speed and cadence data from a peripheral using the standard BLE
Cycling Speed and Cadence (CSC) Service.
"""

import time

import adafruit_ble
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.device_info import DeviceInfoService
from adafruit_ble_cycling_speed_and_cadence import CyclingSpeedAndCadenceService

# PyLint can't find BLERadio for some reason so special case it here.
ble = adafruit_ble.BLERadio()  # pylint: disable=no-member


while True:
    print("Scanning...")
    # Save advertisements, indexed by address
    advs = {}
    for adv in ble.start_scan(ProvideServicesAdvertisement, timeout=5):
        if CyclingSpeedAndCadenceService in adv.services:
            print("found a CyclingSpeedAndCadenceService advertisement")
            # Save advertisement. Overwrite duplicates from same address (device).
            advs[adv.address] = adv

    ble.stop_scan()
    print("Stopped scanning")
    if not advs:
        # Nothing found. Go back and keep looking.
        continue

    # Connect to all available CSC sensors.
    cyc_connections = []
    for adv in advs.values():
        cyc_connections.append(ble.connect(adv))
        print("Connected", len(cyc_connections))

    # Print out info about each sensors.
    for conn in cyc_connections:
        if conn.connected:
            if DeviceInfoService in conn:
                dis = conn[DeviceInfoService]
                try:
                    manufacturer = dis.manufacturer
                except AttributeError:
                    manufacturer = "(Manufacturer Not specified)"
                print("Device:", manufacturer)
            else:
                print("No device information")

    print("Waiting for data... (could be 10-20 seconds or more)")
    # Get CSC Service from each sensor.
    cyc_services = []
    for conn in cyc_connections:
        cyc_services.append(conn[CyclingSpeedAndCadenceService])

    # Read data from each sensor once a second.
    # Stop if we lose connection to all sensors.
    while True:
        still_connected = False
        for conn, svc in zip(cyc_connections, cyc_services):
            if conn.connected:
                still_connected = True
                print(svc.measurement_values)

        if not still_connected:
            break
        time.sleep(1)
