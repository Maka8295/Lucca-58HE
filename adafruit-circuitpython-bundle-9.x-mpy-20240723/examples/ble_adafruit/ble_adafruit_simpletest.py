# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Use with Web Bluetooth Dashboard, or with ble_adafruit_simpletest_client.py

import time

import microcontroller

from adafruit_ble import BLERadio

from adafruit_ble_adafruit.adafruit_service import AdafruitServerAdvertisement
from adafruit_ble_adafruit.temperature_service import TemperatureService

temp_svc = TemperatureService()
temp_svc.measurement_period = 100
temp_last_update = 0

ble = BLERadio()

# Unknown USB PID, since we don't know what board we're on
adv = AdafruitServerAdvertisement()
adv.pid = 0x0000

while True:
    # Advertise when not connected.
    print(adv)
    print(bytes(adv))
    ble.start_advertising(adv)
    while not ble.connected:
        pass
    ble.stop_advertising()

    while ble.connected:
        now_msecs = time.monotonic_ns() // 1000000  # pylint: disable=no-member

        if now_msecs - temp_last_update >= temp_svc.measurement_period:
            temp_svc.temperature = (
                microcontroller.cpu.temperature  # pylint: disable=no-member
            )

            temp_last_update = now_msecs
