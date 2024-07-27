# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Circuit Playground Express CircuitPython Fidget Spinner
# This is meant to work with the Circuit Playground Express board:
#   https://www.adafruit.com/product/3333
# Needs this LIS3DH module and the NeoPixel module installed:
#   https://github.com/adafruit/Adafruit_CircuitPython_LIS3DH
#   https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel
# Author: Tony DiCola
# License: MIT License (https://opensource.org/licenses/MIT)
# pylint: disable=redefined-outer-name
import math
import time

import board
import busio

from micropython import const

import neopixel
import adafruit_lis3dh

# Configuration:
ACCEL_RANGE = adafruit_lis3dh.RANGE_16_G  # Accelerometer range.
TAP_THRESHOLD = 20  # Accelerometer tap threshold.  Higher values
# mean you need to tap harder to start a spin.
SPINNER_DECAY = 0.5  # Decay rate for the spinner.  Set to a value
# from 0 to 1.0 where lower values mean the
# spinner slows down faster.
PRIMARY_COLOR = (0, 255, 0)  # Color of the spinner dots.
SECONDARY_COLOR = (0, 0, 0)  # Background color of the spinner.


# Define a class that represents the fidget spinner.
class FidgetSpinner:
    def __init__(self, decay=0.5):
        self._decay = decay
        self._velocity = 0.0
        self._elapsed = 0.0
        self._position = 0.0

    def spin(self, velocity):
        self._velocity = velocity
        self._elapsed = 0.0

    def get_position(self, delta):
        # Increment elapsed time and compute the current velocity after a
        # decay of the initial velocity.
        self._elapsed += delta
        current_velocity = self._velocity * math.pow(self._decay, self._elapsed)
        self._position += current_velocity * delta
        # Make sure the position stays within values that range from 0 to <10.
        self._position = math.fmod(self._position, 10.0)
        if self._position < 0.0:
            self._position += 10.0
        return self._position


# pylint: disable=no-member
# Initialize NeoPixels and accelerometer.
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, auto_write=False)
pixels.fill((0, 0, 0))
pixels.show()
i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=25)

# Set accelerometer range.
lis3dh.range = ACCEL_RANGE
# Enable single click detection, but use a custom CLICK_CFG register value
# to only detect clicks on the X axis (instead of all 3 X, Y, Z axes).
lis3dh.set_tap(1, TAP_THRESHOLD, click_cfg=0x01)
# Enable LIS3DH FIFO in stream mode.  This reaches in to the LIS3DH library to
# call internal methods that change a few register values.  This must be done
# AFTER calling set_tap above because the set_tap function also changes
# REG_CTRL5.
# Define register numbers, which are not exported from the library.
_REG_CTRL5 = const(0x24)
_REG_CLICKSRC = const(0x39)
# pylint: disable=protected-access
lis3dh._write_register_byte(_REG_CTRL5, 0b01001000)
lis3dh._write_register_byte(0x2E, 0b10000000)  # Set FIFO_CTRL to Stream mode.
# pylint: disable=protected-access

# Create a fidget spinner object.
spinner = FidgetSpinner(SPINNER_DECAY)


# Main loop will run forever checking for click/taps from accelerometer and
# then spinning the spinner.
last = time.monotonic()  # Keep track of the last time the loop ran.
while True:
    # Read the raw click detection register value and check if there was
    # a click detected.
    clicksrc = lis3dh._read_register_byte(
        _REG_CLICKSRC
    )  # pylint: disable=protected-access
    if clicksrc & 0b01000000 > 0:
        # Click was detected!  Quickly read 32 values from the accelerometer
        # FIFO and look for the maximum magnitude values.
        maxval = abs(lis3dh.acceleration[0])  # Grab just the X acceleration value.
        for i in range(31):
            x = abs(lis3dh.acceleration[0])
            if x > maxval:
                maxval = x
        # Check if this was a positive or negative spin/click event.
        if clicksrc == 0b1010001:
            # Positive click, spin in a positive direction.
            spinner.spin(maxval)
        elif clicksrc == 0b1011001:
            # Negative click, spin in negative direction.
            spinner.spin(-maxval)
    # Update the amount of time that's passed since the last loop iteration.
    current = time.monotonic()
    delta = current - last
    last = current
    # Set all pixels to secondary color.
    pixels.fill(SECONDARY_COLOR)
    # Update the fidget spinner position and turn on the appropriate pixels.
    pos = int(spinner.get_position(delta))
    # Set the current position pixel and the pixel exactly opposite it (i.e. 5
    # pixels ahead, wrapping back to the start) to the primary color.
    pixels[pos] = PRIMARY_COLOR
    pixels[(pos + 5) % 10] = PRIMARY_COLOR
    pixels.show()
    # Small delay to stay responsive but give time for interrupt processing.
    time.sleep(0.05)
