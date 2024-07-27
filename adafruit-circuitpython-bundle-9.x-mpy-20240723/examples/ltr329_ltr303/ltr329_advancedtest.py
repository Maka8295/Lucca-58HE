# SPDX-FileCopyrightText: Copyright (c) 2022 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time
import board
import adafruit_ltr329_ltr303 as adafruit_ltr329

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

time.sleep(0.1)  # sensor takes 100ms to 'boot' on power up
ltr329 = adafruit_ltr329.LTR329(i2c)

# Can set the ALS light gain, can be: 1, 2, 4, 8, 48 or 96 times
# to range from 1~64 kLux to 0.01~600 Lux
ltr329.als_gain = 96
print("LTR-329 ALS gain:", ltr329.als_gain)

# Can set the ALS measurement integration time, how long the sensor
# 'looks' for light data. Default is 100ms.
# Set to: 50, 100, 150, 200, 250, 300, 350, or 400 milliseconds
# ltr329.integration_time = 50
print("LTR-329 integration time (ms):", ltr329.integration_time)

# Can set the ALS measurement rate, how often the data register updates
# Default is 500ms. Must be equal or greater than the integration time
# Set to: 50, 100, 200, 500, 1000, 2000 milliseconds
# ltr329.measurement_rate = 500
print("LTR-329 measurement rate (ms):", ltr329.measurement_rate)

# Can put into stand-by mode at any time, for low power usage
# self.active_mode = False

while True:
    # The sensor will let us know when the measurement time has
    # created a new data reading!
    if ltr329.new_als_data_available:
        # The sensor can get 'overwhelmed' by bright light if the
        # gain isn't set right, in which case the data is invalid.
        # We can check the data invalid first and toss out the reading...
        if ltr329.als_data_invalid:
            ltr329.throw_out_reading()  # perform & toss out the reading
            continue  # try again next time!

        # OR we can 'try' to do the read and get an exception if the
        # data is invalid
        try:
            # If we're using `new_als_data_available` we should
            # read both channels ONCE only! To do that use...
            visible_plus_ir, ir = ltr329.light_channels
            # this will get both channels at once! (It's also faster)

            # Now we can do various math...
            print("Visible + IR:", visible_plus_ir)
            print("Infrared    :", ir)
            print("ALS gain:   :", ltr329.als_data_gain)
            print()
        except ValueError:
            # we can also check `ltr329.als_data_invalid` if we
            # want, to verify that
            print("Light sensor data invalid, trying again!")
    time.sleep(0.1)
