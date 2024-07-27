# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This example uses the internal temperature sensor and reports the battery voltage. However, it
   reads the temperature more often but only reports it when it's changed by a degree since the last
   report. When doing a report it will actually do multiple broadcasts and wait 2 ** n readings
   until the next broadcast. The delay is reset every time the temp moves more than 1 degree."""

import math
import time
import analogio
import board
import microcontroller
import adafruit_ble_broadcastnet

print("This is BroadcastNet sensor:", adafruit_ble_broadcastnet.device_address)

battery = analogio.AnalogIn(board.VOLTAGE_MONITOR)
divider_ratio = 2

last_temperature = None
consecutive = 1
while True:
    temp = microcontroller.cpu.temperature  # pylint: disable=no-member
    if not last_temperature or abs(temp - last_temperature) > 1:
        consecutive = 1
        last_temperature = temp
    else:
        consecutive += 1

    # Repeatedly broadcast identical values to help ensure it is picked up by the bridge. Perform
    # exponential backoff as we get more confidence.
    exp = int(math.log(consecutive, 2))
    if 2**exp == consecutive:
        measurement = adafruit_ble_broadcastnet.AdafruitSensorMeasurement()
        battery_voltage = (
            battery.value
            / 2**16
            * divider_ratio
            * battery.reference_voltage  # pylint: disable=no-member
        )
        measurement.battery_voltage = int(battery_voltage * 1000)
        measurement.temperature = temp
        print(measurement)
        adafruit_ble_broadcastnet.broadcast(measurement)

    time.sleep(1)
