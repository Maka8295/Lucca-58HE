# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This example changes the fill, brightness, blink rates,
shows number and text printing, displays a counter
and then shows off the new marquee features."""

from time import sleep
from adafruit_featherwing import sevensegment_featherwing

display = sevensegment_featherwing.SevenSegmentFeatherWing()

# Fill and empty all segments
for count in range(0, 3):
    display.fill(True)
    sleep(0.5)
    display.fill(False)
    sleep(0.5)

# Display a number and text
display.print(1234)
sleep(1)
display.print("FEED")

# Change brightness
for brightness in range(0, 16):
    display.brightness = brightness
    sleep(0.1)

# Change blink rate
for blink_rate in range(3, 0, -1):
    display.blink_rate = blink_rate
    sleep(4)
display.blink_rate = 0

# Show a counter using decimals
count = 975.0
while count < 1025:
    count += 1
    display.print(count)
    sleep(0.1)

# Display a Time
hour = 12
for minute in range(15, 26):
    display.print("{}:{}".format(hour, minute))
    sleep(1)

# Show the Marquee
display.marquee("Deadbeef 192.168.100.102... ", 0.2)
