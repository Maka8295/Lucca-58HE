# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import analogio
import board
import microcontroller
import adafruit_ble_broadcastnet

print("This is BroadcastNet sensor:", adafruit_ble_broadcastnet.device_address)

battery = analogio.AnalogIn(board.VOLTAGE_MONITOR)
divider_ratio = 2

while True:
    measurement = adafruit_ble_broadcastnet.AdafruitSensorMeasurement()
    battery_voltage = (
        battery.value
        / 2**16
        * divider_ratio
        * battery.reference_voltage  # pylint: disable=no-member
    )
    measurement.battery_voltage = int(battery_voltage * 1000)
    measurement.temperature = (
        microcontroller.cpu.temperature  # pylint: disable=no-member
    )
    print(measurement)
    adafruit_ble_broadcastnet.broadcast(measurement)

    time.sleep(30)
