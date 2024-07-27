# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Maps acceleration (tilt) to Neopixel colors.

x, y, and z acceleration components map to red, green and blue,
respectively.

When the Circuit Playground is level, the lights are blue because there is no acceleration
on x or y, but on z, gravity pulls at 9.81 meters per second per second (m/s²).
When banking, the vertical (z) axis is no longer directly aligned with gravity,
so the blue decreases, and red increases because gravity is now pulling more
along the x axis. Similarly, when changing the pitch from level, we see blue change
to green.

This video walks you through the code: https://youtu.be/eNpPLbYx-iA
"""

import time
from adafruit_circuitplayground import cp

cp.pixels.brightness = 0.2  # Adjust overall brightness as desired, between 0 and 1


def color_amount(accel_component):
    """Convert acceleration component (x, y, or z) to color amount (r, g, or b)"""
    standard_gravity = 9.81  # Acceleration (m/s²) due to gravity at the earth’s surface
    accel_magnitude = abs(accel_component)  # Ignore the direction
    constrained_accel = min(accel_magnitude, standard_gravity)  # Constrain values
    normalized_accel = constrained_accel / standard_gravity  # Convert to 0–1
    return round(normalized_accel * 255)  # Convert to 0–255


def format_acceleration():
    return ", ".join(("{:>6.2f}".format(axis_value) for axis_value in acceleration))


def format_rgb():
    return ", ".join(("{:>3d}".format(rgb_amount) for rgb_amount in rgb_amounts))


def log_values():
    print("({}) ==> ({})".format(format_acceleration(), format_rgb()))


while True:
    acceleration = cp.acceleration
    rgb_amounts = [color_amount(axis_value) for axis_value in acceleration]
    cp.pixels.fill(rgb_amounts)
    log_values()
    time.sleep(0.1)
