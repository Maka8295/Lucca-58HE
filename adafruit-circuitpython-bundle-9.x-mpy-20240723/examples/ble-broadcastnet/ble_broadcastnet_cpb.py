# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This uses the CircuitPlayground Bluefruit as a sensor node."""

import time
from adafruit_circuitplayground import cp
import adafruit_ble_broadcastnet

print("This is BroadcastNet sensor:", adafruit_ble_broadcastnet.device_address)

while True:
    measurement = adafruit_ble_broadcastnet.AdafruitSensorMeasurement()

    measurement.temperature = cp.temperature
    measurement.sound_level = cp.sound_level
    measurement.light = cp.light
    measurement.value = cp.switch
    # measurement.acceleration = cp.acceleration

    print(measurement)
    adafruit_ble_broadcastnet.broadcast(measurement)
    time.sleep(60)
