# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import time
import board
from adafruit_ble import BLERadio
from adafruit_ble_adafruit.adafruit_service import AdafruitServerAdvertisement
from adafruit_ble_adafruit.quaternion_service import QuaternionService
from adafruit_bno08x import BNO08X

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
bno = BNO08X(i2c)

quat_svc = QuaternionService()
quat_svc.measurement_period = 50
quat_last_read = 0

ble = BLERadio()

# The Web Bluetooth dashboard identifies known boards by their
# advertised name, not by advertising manufacturer data.
ble.name = "Adafruit Hillcrest Laboratories BNO08x Breakout"

adv = AdafruitServerAdvertisement()
adv.pid = 0x8088

while True:
    # Advertise when not connected.
    ble.start_advertising(adv)
    while not ble.connected:
        pass
    ble.stop_advertising()

    while ble.connected:
        now_msecs = time.monotonic_ns() // 1000000  # pylint: disable=no-member

        if now_msecs - quat_last_read >= quat_svc.measurement_period:
            quat_svc.quaternion = bno.quaternion
            quat_last_read = now_msecs
