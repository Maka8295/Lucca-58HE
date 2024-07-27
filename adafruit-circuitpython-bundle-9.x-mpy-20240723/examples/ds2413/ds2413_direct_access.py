# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example shows how to directly access the DS2413. See the datasheet
# for details. This approach is only recommended for advanced use. For typical
# use, it is suggested to access the pins via the DS2413Pin objects. See the
# simple.py example.
import board
from adafruit_onewire.bus import OneWireBus
import adafruit_ds2413

# Create OneWire bus
ow_bus = OneWireBus(board.D2)

# Create the DS2413 object from the first one found on the bus
ds = adafruit_ds2413.DS2413(ow_bus, ow_bus.scan()[0])

# Get the PIO logical status and report it together with the state of the
# PIO Output Latch
print("0b{:08b}".format(ds.pio_state))

# Control the output transistors. (ON = 0, OFF = 1)
# Turn off both transisotrs
ds.pio_state = 0x03
# Turn on both transisotrs
ds.pio_state = 0x00
# PIOA = on, PIOB = off
ds.pio_state = 0x02
# PIOA = off, PIOB = on
ds.pio_state = 0x01
