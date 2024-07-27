# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example shows how to access the DS2413 pins and use them for both input
# and output. In this example, it is assumed an LED is attached to IOA and a
# button is attached to IOB. See the datasheet for details about how to
# interface the external hardware (it is different than most Arduino examples).
import time
import board
from adafruit_onewire.bus import OneWireBus
import adafruit_ds2413

# Create OneWire bus
ow_bus = OneWireBus(board.D2)

# Create the DS2413 object from the first one found on the bus
ds = adafruit_ds2413.DS2413(ow_bus, ow_bus.scan()[0])

# LED on IOA
led = ds.IOA

# button on IOB
button = ds.IOB
button.direction = adafruit_ds2413.INPUT

# Loop forever
while True:
    # Check for button press
    if button.value:
        # Print a message.
        print("Button pressed!")
        # Toggle LED
        led.value = not led.value
        # A little debounce
        time.sleep(0.25)
