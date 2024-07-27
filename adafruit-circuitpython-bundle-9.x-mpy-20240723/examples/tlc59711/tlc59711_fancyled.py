#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CircuitPython

# SPDX-FileCopyrightText: 2021 s-light
# SPDX-License-Identifier: MIT
# Author Stefan Krüger (s-light)

"""TLC59711 & FancyLED."""

__doc__ = """
TLC59711 & FancyLED.

this is an example for combining the TLC5957 library with FancyLED.
Enjoy the colors :-)
"""

import board

import busio

import adafruit_fancyled.adafruit_fancyled as fancyled
import adafruit_tlc59711

##########################################
print("\n" + (42 * "*") + "\n" + __doc__ + "\n" + (42 * "*") + "\n" + "\n")

##########################################
# print(42 * "*")
# print("initialise digitalio pins for SPI")
# spi_clock = digitalio.DigitalInOut(board.SCK)
# spi_clock.direction = digitalio.Direction.OUTPUT
# spi_mosi = digitalio.DigitalInOut(board.MOSI)
# spi_mosi.direction = digitalio.Direction.OUTPUT
# spi_miso = digitalio.DigitalInOut(board.MISO)
# spi_miso.direction = digitalio.Direction.INPUT

# print((42 * '*') + "\n" + "init busio.SPI")
spi = busio.SPI(board.SCK, MOSI=board.MOSI)

##########################################
print(42 * "*")
print("init TLC5957")
NUM_LEDS = 16
pixels = adafruit_tlc59711.TLC59711(
    spi=spi,
    pixel_count=NUM_LEDS,
)

print("pixel_count", pixels.pixel_count)
print("chip_count", pixels.chip_count)
print("channel_count", pixels.channel_count)


##########################################
# main loop
print(42 * "*")
print("rainbow loop")
hue_offset = 0
while True:
    brightness = 0.8
    color = fancyled.CHSV(hue_offset, 1.0, 1.0)
    color = fancyled.gamma_adjust(color, brightness=brightness)
    pixels.set_pixel_all(color)
    pixels.show()

    # Bigger number = faster spin
    hue_offset += 0.000005
    if hue_offset >= 1:
        hue_offset = 0
        print("heu_offset reset")
