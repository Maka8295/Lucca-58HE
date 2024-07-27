# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Adafruit Service demo for Adafruit CLUE Circuit Playground Bluefruit board.
# Accessible via Adafruit Bluefruit Playground app and Web Bluetooth Dashboard.

import time

import board
from digitalio import DigitalInOut
import neopixel_write

from adafruit_ble import BLERadio

from adafruit_circuitplayground import cp

from adafruit_ble_adafruit.adafruit_service import AdafruitServerAdvertisement

from adafruit_ble_adafruit.accelerometer_service import AccelerometerService
from adafruit_ble_adafruit.addressable_pixel_service import AddressablePixelService
from adafruit_ble_adafruit.button_service import ButtonService
from adafruit_ble_adafruit.light_sensor_service import LightSensorService
from adafruit_ble_adafruit.temperature_service import TemperatureService
from adafruit_ble_adafruit.tone_service import ToneService

accel_svc = AccelerometerService()
accel_svc.measurement_period = 100
accel_last_update = 0

# 3 RGB bytes * 10 pixels.
NEOPIXEL_BUF_LENGTH = 3 * 10
neopixel_svc = AddressablePixelService()
neopixel_buf = bytearray(NEOPIXEL_BUF_LENGTH)
# Take over NeoPixel control from cp.
cp._pixels.deinit()  # pylint: disable=protected-access
neopixel_out = DigitalInOut(board.NEOPIXEL)
neopixel_out.switch_to_output()

button_svc = ButtonService()
button_svc.set_pressed(cp.switch, cp.button_a, cp.button_b)

light_svc = LightSensorService()
light_svc.measurement_period = 100
light_last_update = 0

temp_svc = TemperatureService()
temp_svc.measurement_period = 100
temp_last_update = 0

tone_svc = ToneService()

ble = BLERadio()
# The Web Bluetooth dashboard identifies known boards by their
# advertised name, not by advertising manufacturer data.
ble.name = "CPlay"

# The Bluefruit Playground app looks in the manufacturer data
# in the advertisement. That data uses the USB PID as a unique ID.
# Adafruit Circuit Playground Bluefruit USB PID:
# Arduino: 0x8045,  CircuitPython: 0x8046, app supports either
adv = AdafruitServerAdvertisement()
adv.pid = 0x8046

while True:
    # Advertise when not connected.
    ble.start_advertising(adv)
    while not ble.connected:
        pass
    ble.stop_advertising()

    while ble.connected:
        now_msecs = time.monotonic_ns() // 1000000  # pylint: disable=no-member

        if now_msecs - accel_last_update >= accel_svc.measurement_period:
            accel_svc.acceleration = cp.acceleration
            accel_last_update = now_msecs

        button_svc.set_pressed(cp.switch, cp.button_a, cp.button_b)

        if now_msecs - light_last_update >= light_svc.measurement_period:
            light_svc.light_level = cp.light
            light_last_update = now_msecs

        neopixel_values = neopixel_svc.values
        if neopixel_values is not None:
            start = neopixel_values.start
            if start > NEOPIXEL_BUF_LENGTH:
                continue
            data = neopixel_values.data
            data_len = min(len(data), NEOPIXEL_BUF_LENGTH - start)
            neopixel_buf[start : start + data_len] = data[:data_len]
            if neopixel_values.write_now:
                neopixel_write.neopixel_write(neopixel_out, neopixel_buf)

        if now_msecs - temp_last_update >= temp_svc.measurement_period:
            temp_svc.temperature = cp.temperature
            temp_last_update = now_msecs

        tone = tone_svc.tone
        if tone is not None:
            freq, duration_msecs = tone
            if freq != 0:
                if duration_msecs != 0:
                    # Note that this blocks. Alternatively we could
                    # use now_msecs to time a tone in a non-blocking
                    # way, but then the other updates might make the
                    # tone interval less consistent.
                    cp.play_tone(freq, duration_msecs / 1000)
                else:
                    cp.stop_tone()
                    cp.start_tone(freq)
            else:
                cp.stop_tone()
        last_tone = tone
