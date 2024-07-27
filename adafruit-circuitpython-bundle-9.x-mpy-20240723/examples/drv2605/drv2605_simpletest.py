# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of the DRV2605 haptic feedback motor driver.
# Will play all 123 effects in order for about a half second each.
import time

import board
import busio

import adafruit_drv2605


# Initialize I2C bus and DRV2605 module.
i2c = busio.I2C(board.SCL, board.SDA)
drv = adafruit_drv2605.DRV2605(i2c)

# Main loop runs forever trying each effect (1-123).
# See table 11.2 in the datasheet for a list of all the effect names and IDs.
#   http://www.ti.com/lit/ds/symlink/drv2605.pdf
effect_id = 1
while True:
    print("Playing effect #{0}".format(effect_id))
    drv.sequence[0] = adafruit_drv2605.Effect(effect_id)  # Set the effect on slot 0.
    # You can assign effects to up to 8 different slots to combine
    # them in interesting ways. Index the sequence property with a
    # slot number 0 to 7.
    # Optionally, you can assign a pause to a slot. E.g.
    # drv.sequence[1] = adafruit_drv2605.Pause(0.5)  # Pause for half a second
    drv.play()  # play the effect
    time.sleep(0.5)  # for 0.5 seconds
    drv.stop()  # and then stop (if it's still running)
    # Increment effect ID and wrap back around to 1.
    effect_id += 1
    if effect_id > 123:
        effect_id = 1
