# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Gravity Pulls Pixel

This program uses the Circuit Playground's accelerometer to position
a white pixel as if gravity were pulling it.

Flip the switch left (toward the notes) to turn on debugging messages and
slow down the action. See a code walkthrough here: https://youtu.be/sZ4tNOUKRpw
"""
import time
import math
from adafruit_circuitplayground import cp

PIXEL_SPACING_ANGLE = 30
STANDARD_GRAVITY = 9.81

BACKGROUND_COLOR = 0, 0, 64
MIN_BRIGHTNESS = 15  # Minimum brightness for anti-aliasing
LIGHTING_ARC_LENGTH = 45


def compute_pixel_angles():
    """Return a list of rotation angles of the ten NeoPixels.

    On the Circuit Playground there are ten pixels arranged like the 12 hours of a clock, except
    that positions 6 and 12 are empty. The numbers in the list are the angles from the (x, y)
    accelerometer values for each pixel when the Circuit Playground is rotated with that pixel at
    the bottom. For example, with pixel 0 at the bottom (and pixel 5 at the top), the
    accelerometer’s (x, y) values give an angle of 300°. Rotated clockwise 1/12 turn (30°), so
    that pixel 1 is at the bottom, the angle is 330°.
    """
    return [
        (300 + PIXEL_SPACING_ANGLE * n) % 360 for n in range(12) if n not in (5, 11)
    ]


def degrees_between(a1, a2):
    smaller = min(a1, a2)
    larger = max(a1, a2)
    return min(larger - smaller, 360 + smaller - larger)


def pixel_brightness(distance_from_down, accel_magnitude):
    """Return the a brightness for a pixel, or None if the pixel is not in the lighting arc"""
    half_lighting_arc_length = LIGHTING_ARC_LENGTH / 2

    if accel_magnitude < 0.1 or distance_from_down > half_lighting_arc_length:
        return None

    normalized_nearness = 1 - distance_from_down / half_lighting_arc_length
    scale_factor = (255 - MIN_BRIGHTNESS) * accel_magnitude
    color_part = MIN_BRIGHTNESS + round(normalized_nearness * scale_factor)
    return color_part


def angle_in_degrees(x, y):
    """Return the angle of the point (x, y), in degrees from -180 to 180"""
    return math.atan2(y, x) / math.pi * 180


def positive_degrees(angle):
    """Convert -180 through 180 to 0 through 360"""
    return (angle + 360) % 360


cp.pixels.brightness = 0.1  # Adjust overall brightness as desired, between 0 and 1
pixel_positions = compute_pixel_angles()

while True:
    debug = cp.switch  # True is toward the left
    accel_x, accel_y = cp.acceleration[:2]  # Ignore z
    down_angle = positive_degrees(angle_in_degrees(accel_x, accel_y))
    magnitude_limit = STANDARD_GRAVITY
    normalized_magnitude = (
        min(math.sqrt(accel_x * accel_x + accel_y * accel_y), magnitude_limit)
        / magnitude_limit
    )

    pixels_lit = []
    for i, pixel_position in enumerate(pixel_positions):
        pe = pixel_brightness(
            degrees_between(pixel_position, down_angle), normalized_magnitude
        )
        cp.pixels[i] = (pe, pe, pe) if pe else BACKGROUND_COLOR
        if pe:
            pixels_lit.append((i, pe))

    if debug:
        lit_formatted = ", ".join(("{}: {:>3d}".format(p, i) for p, i in pixels_lit))
        print(
            "x: {:>6.2f}, y: {:>6.2f}, angle: {:>6.2f}, mag: {:>3.2f}, pixels: [{}]".format(
                accel_x, accel_y, down_angle, normalized_magnitude, lit_formatted
            )
        )
        time.sleep(0.5)
