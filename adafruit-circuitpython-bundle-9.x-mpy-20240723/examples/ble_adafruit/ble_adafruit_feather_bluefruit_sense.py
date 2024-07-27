# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Adafruit Service demo for Adafruit Feather Bluefruit Sense board.
# Accessible via Adafruit Web Bluetooth Dashboard.
# (As of this writing, not yet accessible via Bluefruit Playground app.)

import time

import board

import digitalio
import neopixel_write

from ulab import numpy as np

from adafruit_ble import BLERadio

import audiobusio

import adafruit_apds9960.apds9960
import adafruit_bmp280
import adafruit_lsm6ds.lsm6ds33
import adafruit_sht31d

from adafruit_ble_adafruit.adafruit_service import AdafruitServerAdvertisement

from adafruit_ble_adafruit.accelerometer_service import AccelerometerService
from adafruit_ble_adafruit.addressable_pixel_service import AddressablePixelService
from adafruit_ble_adafruit.barometric_pressure_service import BarometricPressureService
from adafruit_ble_adafruit.button_service import ButtonService
from adafruit_ble_adafruit.humidity_service import HumidityService
from adafruit_ble_adafruit.light_sensor_service import LightSensorService
from adafruit_ble_adafruit.microphone_service import MicrophoneService
from adafruit_ble_adafruit.temperature_service import TemperatureService

# Accelerometer
lsm6ds33 = adafruit_lsm6ds.lsm6ds33.LSM6DS33(board.I2C())
# Used for pressure and temperature.
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(board.I2C())
# Humidity.
sht31d = adafruit_sht31d.SHT31D(board.I2C())
# Used only for light sensor
apds9960 = adafruit_apds9960.apds9960.APDS9960(board.I2C())
apds9960.enable_color = True

mic = audiobusio.PDMIn(
    board.MICROPHONE_CLOCK,
    board.MICROPHONE_DATA,
    sample_rate=16000,
    bit_depth=16,
)

# Create and initialize the available services.

accel_svc = AccelerometerService()
accel_svc.measurement_period = 100
accel_last_update = 0

# Feather Bluefruit Sense has just one board pixel. 3 RGB bytes * 1 pixel
NEOPIXEL_BUF_LENGTH = 3 * 1
neopixel_svc = AddressablePixelService()
neopixel_buf = bytearray(NEOPIXEL_BUF_LENGTH)
neopixel_out = digitalio.DigitalInOut(board.NEOPIXEL)
neopixel_out.switch_to_output()

baro_svc = BarometricPressureService()
baro_svc.measurement_period = 100
baro_last_update = 0

button_svc = ButtonService()
button = digitalio.DigitalInOut(board.SWITCH)
button.pull = digitalio.Pull.UP
button_svc.set_pressed(False, not button.value, False)

humidity_svc = HumidityService()
humidity_svc.measurement_period = 100
humidity_last_update = 0

light_svc = LightSensorService()
light_svc.measurement_period = 100
light_last_update = 0

# Send 256 16-bit samples at a time.
MIC_NUM_SAMPLES = 256
mic_svc = MicrophoneService()
mic_svc.number_of_channels = 1
mic_svc.measurement_period = 100
mic_last_update = 0
mic_samples = np.zeros(MIC_NUM_SAMPLES, dtype=np.uint16)

temp_svc = TemperatureService()
temp_svc.measurement_period = 100
temp_last_update = 0

ble = BLERadio()
# The Web Bluetooth dashboard identifies known boards by their
# advertised name, not by advertising manufacturer data.
ble.name = "Sense"

# The Bluefruit Playground app looks in the manufacturer data
# in the advertisement. That data uses the USB PID as a unique ID.
# Feather Bluefruit Sense USB PID:
# This board is not yet support on the app.
# Arduino: 0x8087,  CircuitPython: 0x8088
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

        if now_msecs - accel_last_update >= accel_svc.measurement_period:
            accel_svc.acceleration = lsm6ds33.acceleration
            accel_last_update = now_msecs

        if now_msecs - baro_last_update >= baro_svc.measurement_period:
            baro_svc.pressure = bmp280.pressure
            baro_last_update = now_msecs

        button_svc.set_pressed(False, not button.value, False)

        if now_msecs - humidity_last_update >= humidity_svc.measurement_period:
            humidity_svc.humidity = sht31d.relative_humidity
            humidity_last_update = now_msecs

        if now_msecs - light_last_update >= light_svc.measurement_period:
            # Return "clear" color value from color sensor.
            light_svc.light_level = apds9960.color_data[3]
            light_last_update = now_msecs

        if now_msecs - mic_last_update >= mic_svc.measurement_period:
            mic.record(mic_samples, len(mic_samples))
            # This subtraction yields unsigned values which are
            # reinterpreted as signed after passing.
            mic_svc.sound_samples = mic_samples - 32768
            mic_last_update = now_msecs

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
            temp_svc.temperature = bmp280.temperature
            temp_last_update = now_msecs
