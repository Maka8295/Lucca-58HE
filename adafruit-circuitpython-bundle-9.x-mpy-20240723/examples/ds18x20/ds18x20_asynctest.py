# SPDX-FileCopyrightText: 2020 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of printing the temperature from the first found DS18x20 sensor every second.
# Using the asynchronous functions start_temperature_read() and
# read_temperature() to allow the main loop to keep processing while
# the conversion is in progress.
# Author: Louis Bertrand, based on original by Tony DiCola

# A 4.7Kohm pullup between DATA and POWER is REQUIRED!

import time
import board
from adafruit_onewire.bus import OneWireBus
from adafruit_ds18x20 import DS18X20


# Initialize one-wire bus on board pin D1.
ow_bus = OneWireBus(board.D1)

# Scan for sensors and grab the first one found.
ds18 = DS18X20(ow_bus, ow_bus.scan()[0])
ds18.resolution = 12

# Main loop to print the temperature every second.
while True:
    conversion_delay = ds18.start_temperature_read()
    conversion_ready_at = time.monotonic() + conversion_delay
    print("waiting", end="")
    while time.monotonic() < conversion_ready_at:
        print(".", end="")
        time.sleep(0.1)
    print("\nTemperature: {0:0.3f}C\n".format(ds18.read_temperature()))
    time.sleep(1.0)
