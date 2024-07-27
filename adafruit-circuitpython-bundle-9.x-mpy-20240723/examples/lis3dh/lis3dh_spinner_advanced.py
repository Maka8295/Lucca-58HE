# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Circuit Playground Express CircuitPython Advanced Fidget Spinner
#
# This is a more advanced version of the fidget spinner which lets you change
# color and animation type by pressing either the A or B buttons.  NOTE: you
# cannot run this example with a tool like ampy and MUST copy it to the board
# and name it main.py to run at boot.
#
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
import digitalio

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
# Define list of color combinations.  Pressing button A will cycle through
# these combos.  Each tuple entry (line) should be a 2-tuple of 3-tuple RGB
# values (0-255).
COLORS = (
    ((255, 0, 0), (0, 0, 0)),  # Red to black
    ((0, 255, 0), (0, 0, 0)),  # Green to black
    ((0, 0, 255), (0, 0, 0)),  # Blue to black
    ((255, 0, 0), (0, 255, 0)),  # Red to green
    ((255, 0, 0), (0, 0, 255)),  # Red to blue
    ((0, 255, 0), (0, 0, 255)),  # Green to blue
)


# Helper functions:
def lerp(x, x0, x1, y0, y1):
    """Linearly interpolate a value y given range y0...y1 that is proportional
    to x in range x0...x1 .
    """
    return y0 + (x - x0) * ((y1 - y0) / (x1 - x0))


def color_lerp(x, x0, x1, c0, c1):
    """Linearly interpolate RGB colors (3-tuples of byte values) given x
    in range x0...x1.
    """
    r0, g0, b0 = c0
    r1, g1, b1 = c1
    return (
        int(lerp(x, x0, x1, r0, r1)),
        int(lerp(x, x0, x1, g0, g1)),
        int(lerp(x, x0, x1, b0, b1)),
    )


# Define a class that represents the fidget spinner.  The spinner only has a
# concept of its current position, a continuous value from 0 to <10.  You can
# start spinning the spinner with an initial velocity by calling the spin
# function, then periodically call get_position to get the current spinner
# position.  Since the position moves between values 0 to 10 it can easily map
# to pixel positions around the Circuit Playground Express board.
class FidgetSpinner:
    def __init__(self, decay=0.5):
        """Create an instance of the fidget spinner.  Specify the decay rate
        as a value from 0 to 1 (continuous, floating point)--lower decay rate
        values will cause the spinner to slow down faster.
        """
        self._decay = decay
        self._velocity = 0.0
        self._elapsed = 0.0
        self._position = 0.0

    def spin(self, velocity):
        """Start the spinner moving at the specified initial velocity (in
        positions/second).
        """
        self._velocity = velocity
        self._elapsed = 0.0

    def get_position(self, delta):
        """Update the spinner position after the specified delta (in seconds)
        has elapsed.  Will return the new spinner position, a continuous value
        from 0...<10.
        """
        # Increment elapsed time and compute the current velocity after a
        # decay of the initial velocity.
        self._elapsed += delta
        current_velocity = self._velocity * math.pow(self._decay, self._elapsed)
        # Update position based on the current_velocity and elapsed time.
        self._position += current_velocity * delta
        # Make sure the position stays within values that range from 0 to <10.
        self._position = math.fmod(self._position, 10.0)
        if self._position < 0.0:
            self._position += 10.0
        return self._position


# Define animation classes.  Each animation needs to have an update function
# which takes in the current spinner position and a selected primary and
# secondary color (3-tuple of RGB bytes) and will render a frame of spinner
# animation.
class DiscreteDotAnimation:
    def __init__(self, pixels, dots=2):
        """Create an instance of a simple discrete dot animation.  The dots
        parameter controls how many dots are rendered on the display (each
        evenly spaced apart).
        """
        self._pixels = pixels
        self._dots = dots
        self._dot_offset = pixels.n / self._dots

    def update(self, position, primary, secondary):
        """Update the animation given the current spinner position and
        selected primary and secondary colors.
        """
        # Clear all the pixels to secondary colors, then draw a number of
        # dots evenly spaced around the pixels and starting at the provided
        # position.
        self._pixels.fill(secondary)
        for i in range(self._dots):
            pos = int(position + i * self._dot_offset) % self._pixels.n
            self._pixels[pos] = primary
        self._pixels.show()


class SmoothAnimation:
    def __init__(self, pixels, frequency=2.0):
        """Create an instance of a smooth sine-wave based animation that sweeps
        around the board based on spinner position.  Frequency specifies how
        many primary to secondary color bumps are shown around the board.
        """
        self._pixels = pixels
        # Precompute some of the sine wave math factors so they aren't
        # recomputed in every loop iteration.
        self._sin_scale = 2.0 * math.pi * frequency / pixels.n
        self._phase_scale = 2.0 * math.pi / 10.0

    def update(self, position, primary, secondary):
        """Update the animation given the current spinner position and
        selected primary and secondary colors.
        """
        # Draw a smooth sine wave of primary and secondary color moving around
        # the pixels.  Each pixel color is computed based on interpolating
        # color based on its position around the board, and a phase offset that
        # changes based on fidget spinner position.
        phase = self._phase_scale * position
        for i in range(self._pixels.n):
            x = math.sin(self._sin_scale * i - phase)
            self._pixels[i] = color_lerp(x, -1.0, 1.0, primary, secondary)
        self._pixels.show()


# pylint: disable=no-member
# Initialize and turn off NeoPixels.
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, auto_write=False)
pixels.fill((0, 0, 0))
pixels.show()

# Initialize buttons.
button_a = digitalio.DigitalInOut(board.BUTTON_A)
button_a.switch_to_input(pull=digitalio.Pull.DOWN)
button_b = digitalio.DigitalInOut(board.BUTTON_B)
button_b.switch_to_input(pull=digitalio.Pull.DOWN)

# Initialize the LIS3DH accelerometer.
# Note that this is specific to Circuit Playground Express boards.  For other
# uses change the SCL and SDA pins below, and optionally the address of the
# device if needed.
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
# REG_CTRL5.  The FIFO stream mode will keep track of the 32 last X,Y,Z accel
# readings in a FIFO buffer so they can be read later to see a history of
# recent acceleration.  This is handy to look for the maximum/minimum impulse
# after a click is detected.
# Define register numbers, which are not exported from the library.
_REG_CTRL5 = const(0x24)
_REG_CLICKSRC = const(0x39)
# pylint: disable=protected-access
lis3dh._write_register_byte(_REG_CTRL5, 0b01001000)
lis3dh._write_register_byte(0x2E, 0b10000000)  # Set FIFO_CTRL to Stream mode.
# pylint: disable=protected-access

# Create a fidget spinner object.
spinner = FidgetSpinner(SPINNER_DECAY)

# Other global state for the spinner animation:
last = time.monotonic()  # Keep track of the last time the loop ran.
color_index = 0  # Keep track of the currently selected color combo.
animations = (
    DiscreteDotAnimation(pixels, 1),  # Define list of animations.
    DiscreteDotAnimation(pixels, 2),  # Button B presses cycle
    SmoothAnimation(pixels, 1),  # through these animations.
    SmoothAnimation(pixels, 2),
)
animation_index = 0  # Keep track of currently selected animation.

# Main loop will run forever checking for click/taps from accelerometer and
# then spinning the spinner.
while True:
    # Check for button press at the top and bottom of the loop so some time
    # elapses and the change in button state from pressed to released can be
    # detected.
    initial_a = button_a.value
    initial_b = button_b.value
    # Read the raw click detection register value and check if there was
    # a click detected.  Remember only the X axis causes clicks because of
    # the register configuration set previously.
    clicksrc = lis3dh._read_register_byte(
        _REG_CLICKSRC
    )  # pylint: disable=protected-access
    if clicksrc & 0b01000000 > 0:
        # Click was detected!  Quickly read 32 values from the accelerometer
        # and look for the maximum magnitude values.  Because the
        # accelerometer is in FIFO stream mode it will keep a history of the
        # 32 last accelerometer readings and return them when consecutively
        # read.
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
    # Update fidget spinner position.
    position = spinner.get_position(delta)
    # Grab the currently selected primary and secondary colors.
    primary = COLORS[color_index][0]
    secondary = COLORS[color_index][1]
    # Draw the current animation on the pixels.
    animations[animation_index].update(position, primary, secondary)
    # Small delay to stay responsive but give time for interrupt processing.
    time.sleep(0.01)
    # Check button state again and compare to initial state to see if there
    # was a change (i.e. button was released).
    if not button_a.value and initial_a:
        # Button a released, i.e. it was true (high) and now is false (low).
        # Increment color and wrap back to zero when beyond total # of colors.
        color_index = (color_index + 1) % len(COLORS)
    if not button_b.value and initial_b:
        # Button b released, i.e. it was true (high) and now is false (low).
        # Increment animation (wrapping back around to zero as necessary).
        animation_index = (animation_index + 1) % len(animations)
