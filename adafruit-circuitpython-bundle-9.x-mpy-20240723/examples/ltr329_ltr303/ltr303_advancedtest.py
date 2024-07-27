# SPDX-FileCopyrightText: Copyright (c) 2022 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time
import board
import adafruit_ltr329_ltr303 as adafruit_ltr303

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

time.sleep(0.1)  # sensor takes 100ms to 'boot' on power up
ltr303 = adafruit_ltr303.LTR303(i2c)

# Can set the ALS light gain, can be: 1, 2, 4, 8, 48 or 96 times
# to range from 1~64 kLux to 0.01~600 Lux
ltr303.als_gain = 96
print("LTR-303 ALS gain:", ltr303.als_gain)

# Can set the ALS measurement integration time, how long the sensor
# 'looks' for light data. Default is 100ms.
# Set to: 50, 100, 150, 200, 250, 300, 350, or 400 millisec
# ltr303.integration_time = 50
print("LTR-303 integration time (ms):", ltr303.integration_time)

# Can set the ALS measurement rate, how often the data register updates
# Default is 500ms. Must be equal or greater than the integration time
# Set to: 50, 100, 200, 500, 1000, 2000 millisec
# ltr303.measurement_rate = 500
print("LTR-303 measurement rate (ms):", ltr303.measurement_rate)

# Can put into stand-by mode at any time, for low power usage
# self.active_mode = False

# The LTR-303, unlike the LTR-329, can also generate an IRQ output
# The interrupt output can be enabled
ltr303.enable_int = True
# We can also change whether the polarity is active LOW (False) or HIGH (True)
# Default is LOW (False)
ltr303.int_polarity = False

# Then set the low and high thresholds that would trigger an IRQ!
ltr303.threshold_low = 2000  # interrupt goes off if BELOW this number
ltr303.threshold_high = 40000  # or ABOVE this number!
print("Interrupt thresholds:", ltr303.threshold_low, ltr303.threshold_high)

# Finally, we can set how many measurements must be above/below before
# we trigger an IRQ - basically avoid spurious readings. A setting of 1
# means every value triggers an int, 2 means two consecutive readings to
# trigger... up to 16!
ltr303.int_persistence = 4

while True:
    # The sensor will let us know when the measurement time has
    # created a new data reading!
    if ltr303.new_als_data_available:
        # The sensor can get 'overwhelmed' by bright light if the
        # gain isn't set right, in which case the data is invalid.
        # We can check the data invalid first and toss out the reading...
        if ltr303.als_data_invalid:
            ltr303.throw_out_reading()  # perform & toss out the reading
            continue  # try again next time!

        # OR we can 'try' to do the read and get an exception if the
        # data is invalid
        try:
            # If we're using `new_als_data_available` we should
            # read both channels ONCE only! To do that use...
            visible_plus_ir, ir = ltr303.light_channels
            # this will get both channels at once! (It's also faster)

            # Now we can do various math...
            print("Visible + IR:", visible_plus_ir)
            print("Infrared    :", ir)
            print("ALS gain:   :", ltr303.als_data_gain)
            print()
        except ValueError:
            # we can also check `ltr303.als_data_invalid` if we
            # want, to verify that
            print("Light sensor data invalid, trying again!")
    time.sleep(0.1)
