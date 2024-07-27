# SPDX-FileCopyrightText: 2020 by Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
# pylint:disable=unused-import,no-member

import time
import board
from adafruit_ltr390 import LTR390, MeasurementDelay, Resolution, Gain

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
ltr = LTR390(i2c)

# ltr.resolution = Resolution.RESOLUTION_16BIT
print("Measurement resolution is", Resolution.string[ltr.resolution])

# ltr.gain = Gain.GAIN_1X
print("Measurement gain is", Gain.string[ltr.gain])

# ltr.measurement_delay = MeasurementDelay.DELAY_100MS
print("Measurement delay is", MeasurementDelay.string[ltr.measurement_delay])
print("")
while True:
    print("UV:", ltr.uvs, "\t\tAmbient Light:", ltr.light)

    # for shorter measurement delays you may need to make this sleep shorter to see a change
    time.sleep(1.0)
