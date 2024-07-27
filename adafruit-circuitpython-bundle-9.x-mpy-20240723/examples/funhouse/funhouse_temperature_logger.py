# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
This example demonstrates how to log temperature on the FunHouse. Due to the sensors being near the
power supply, usage of peripherals generates extra heat. By turning off unused peripherals and back
on only during usage, it can lower the heat. Using light sleep in between readings will also help.
By using an offset, we can improve the accuracy even more. Improving airflow near the FunHouse will
also help.
"""

from adafruit_funhouse import FunHouse

funhouse = FunHouse(default_bg=None)

DELAY = 180
FEED = "temperature"
TEMPERATURE_OFFSET = (
    3  # Degrees C to adjust the temperature to compensate for board produced heat
)

# Turn things off
funhouse.peripherals.dotstars.fill(0)
funhouse.display.brightness = 0
funhouse.network.enabled = False


def log_data():
    print("Logging Temperature")
    print("Temperature %0.1F" % (funhouse.peripherals.temperature - TEMPERATURE_OFFSET))
    # Turn on WiFi
    funhouse.network.enabled = True
    # Connect to WiFi
    funhouse.network.connect()
    # Push to IO using REST
    funhouse.push_to_io(FEED, funhouse.peripherals.temperature - TEMPERATURE_OFFSET)
    # Turn off WiFi
    funhouse.network.enabled = False


while True:
    log_data()
    print("Sleeping for {} seconds...".format(DELAY))
    funhouse.enter_light_sleep(DELAY)
