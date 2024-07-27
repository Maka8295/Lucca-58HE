# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This is a basic sensor node that uses the internal temperature sensor and reports it every 10
   seconds."""

import time
import microcontroller
import adafruit_ble_broadcastnet

print("This is BroadcastNet sensor:", adafruit_ble_broadcastnet.device_address)

while True:
    measurement = adafruit_ble_broadcastnet.AdafruitSensorMeasurement()
    measurement.temperature = (
        microcontroller.cpu.temperature  # pylint: disable=no-member
    )
    print(measurement)
    adafruit_ble_broadcastnet.broadcast(measurement)
    time.sleep(10)
