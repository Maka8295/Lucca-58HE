# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import analogio
import board
import microcontroller
import neopixel
import adafruit_ble_broadcastnet

print("This is BroadcastNet sensor:", adafruit_ble_broadcastnet.device_address)

battery = analogio.AnalogIn(board.VOLTAGE_MONITOR)
divider_ratio = 2

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

while True:
    measurement = adafruit_ble_broadcastnet.AdafruitSensorMeasurement()
    battery_voltage = (
        battery.value
        / 2**16
        * divider_ratio
        * battery.reference_voltage  # pylint: disable=no-member
    )
    r = 16 - int(((battery_voltage - 3.6) / 0.6) * 16)
    r = min(16, max(r, 0))
    g = int(((battery_voltage - 3.6) / 0.6) * 16)
    g = min(16, max(g, 0))
    pixel[0] = r << 16 | g << 8
    measurement.battery_voltage = int(battery_voltage * 1000)
    measurement.temperature = (
        microcontroller.cpu.temperature  # pylint: disable=no-member
    )
    print(measurement)
    adafruit_ble_broadcastnet.broadcast(measurement)
    pixel[0] = 0

    time.sleep(30)
