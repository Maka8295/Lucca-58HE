# SPDX-FileCopyrightText: 2019 Dave Astels for Adafruit Industries
# SPDX-License-Identifier: MIT

# pylint: disable=invalid-name

# Wait for a falling transition on the clock (signal 1)
# When it's seen, display the values of signal 2-5
# Demonstrates debouncing a lambda predicate

import time
from adafruit_crickit import crickit
from adafruit_debouncer import Debouncer

ss = crickit.seesaw


def make_crikit_signal_debouncer(pin):
    """Return a lambda to read the specified pin"""
    ss.pin_mode(pin, ss.INPUT_PULLUP)
    return Debouncer(lambda: ss.digital_read(pin))


# Two buttons are pullups, connect to ground to activate
clock = make_crikit_signal_debouncer(crickit.SIGNAL1)
signal_2 = make_crikit_signal_debouncer(crickit.SIGNAL2)
signal_3 = make_crikit_signal_debouncer(crickit.SIGNAL3)
signal_4 = make_crikit_signal_debouncer(crickit.SIGNAL4)
signal_5 = make_crikit_signal_debouncer(crickit.SIGNAL5)

while True:
    clock.update()
    signal_2.update()
    signal_3.update()
    signal_4.update()
    signal_5.update()

    if clock.fell:
        print(
            "%u %u %u %u"
            % (signal_2.value, signal_3.value, signal_4.value, signal_5.value)
        )

    time.sleep(0.1)
