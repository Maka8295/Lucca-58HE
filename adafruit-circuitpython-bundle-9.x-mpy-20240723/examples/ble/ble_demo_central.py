# SPDX-FileCopyrightText: 2020 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Demonstration of a Bluefruit BLE Central for Circuit Playground Bluefruit. Connects to the first BLE
UART peripheral it finds. Sends Bluefruit ColorPackets, read from three accelerometer axis, to the
peripheral.
"""

import time

import board
import busio
import digitalio
import adafruit_lis3dh
import neopixel

from adafruit_bluefruit_connect.color_packet import ColorPacket

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService


def scale(value):
    """Scale an value from  (acceleration range) to 0-255 (RGB range)"""
    value = abs(value)
    value = max(min(19.6, value), 0)
    return int(value / 19.6 * 255)


i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
int1 = digitalio.DigitalInOut(board.ACCELEROMETER_INTERRUPT)
accelerometer = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19, int1=int1)
accelerometer.range = adafruit_lis3dh.RANGE_8_G

neopixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.1)

ble = BLERadio()

uart_connection = None
# See if any existing connections are providing UARTService.
if ble.connected:
    for connection in ble.connections:
        if UARTService in connection:
            uart_connection = connection
        break

while True:
    if not uart_connection:
        print("Scanning...")
        for adv in ble.start_scan(ProvideServicesAdvertisement, timeout=5):
            if UARTService in adv.services:
                print("found a UARTService advertisement")
                uart_connection = ble.connect(adv)
                break
        # Stop scanning whether or not we are connected.
        ble.stop_scan()

    while uart_connection and uart_connection.connected:
        r, g, b = map(scale, accelerometer.acceleration)

        color = (r, g, b)
        neopixels.fill(color)
        color_packet = ColorPacket(color)
        try:
            uart_connection[UARTService].write(color_packet.to_bytes())
        except OSError:
            try:
                uart_connection.disconnect()
            except:  # pylint: disable=bare-except
                pass
            uart_connection = None
        time.sleep(0.3)
