# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

### Based on example from
### https://github.com/adafruit/Adafruit_CircuitPython_DotStar/tree/master/examples

import time
import random
import board
import adafruit_ws2801

### Example for a Feather M4 driving 25 12mm leds
odata = board.D5
oclock = board.D6
numleds = 25
bright = 1.0
leds = adafruit_ws2801.WS2801(
    oclock, odata, numleds, brightness=bright, auto_write=False
)

######################### HELPERS ##############################


# a random color 0 -> 224
def random_color():
    return random.randrange(0, 7) * 32


######################### MAIN LOOP ##############################
n_leds = len(leds)
while True:
    # fill each led with a random color
    for idx in range(n_leds):
        leds[idx] = (random_color(), random_color(), random_color())

    # show all leds in led string
    leds.show()

    time.sleep(0.25)
