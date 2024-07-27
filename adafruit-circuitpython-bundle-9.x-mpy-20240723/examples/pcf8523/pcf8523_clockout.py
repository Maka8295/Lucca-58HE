# SPDX-FileCopyrightText: 2023 Bernhard Bablok
# SPDX-License-Identifier: MIT

# Simple demo for clockout-mode (square-wave generation)
# Note that for 32kHz, the duty-cycle is from 60:40 to 40:60, thus
# it is not a perfect square wave (see datasheet 8.9.1.2)

import time
import board
import busio
import countio
from digitalio import Pull
from adafruit_pcf8523.clock import Clock

PIN_SDA = board.GP2  # connect to RTC
PIN_SCL = board.GP3  # connect to RTC
# use board.SCL and board.SDA if available

i2c = busio.I2C(PIN_SCL, PIN_SDA)
# or i2c = board.I2C() if available
clock = Clock(i2c)

# pin must support countio
PIN_COUT = board.GP5
counter = countio.Counter(pin=PIN_COUT, edge=countio.Edge.RISE, pull=Pull.UP)
DURATION = 10

# Main loop:
while True:
    # disable clockout
    print(f"testing disabled clock for {DURATION} seconds")
    clock.clockout_frequency = clock.CLOCKOUT_FREQ_DISABLED
    counter.reset()
    time.sleep(DURATION)
    print(f"clock-pulses: {counter.count}")
    print(f"clock-freq:   {counter.count/DURATION}")

    # test 32kHz
    print(f"testing 32 kHz clock for {DURATION} seconds")
    clock.clockout_frequency = clock.CLOCKOUT_FREQ_32KHZ
    counter.reset()
    time.sleep(DURATION)
    clock.clockout_frequency = clock.CLOCKOUT_FREQ_DISABLED
    print(f"clock-pulses: {counter.count}")
    print(f"clock-freq:   {counter.count/DURATION}")

    # test 4kHz
    print(f"testing 4 kHz clock for {DURATION} seconds")
    clock.clockout_frequency = clock.CLOCKOUT_FREQ_4KHZ
    counter.reset()
    time.sleep(DURATION)
    clock.clockout_frequency = clock.CLOCKOUT_FREQ_DISABLED
    print(f"clock-pulses: {counter.count}")
    print(f"clock-freq:   {counter.count/DURATION}")

    # test 1Hz
    print(f"testing 1 Hz clock for {DURATION} seconds")
    clock.clockout_frequency = clock.CLOCKOUT_FREQ_1HZ
    counter.reset()
    time.sleep(DURATION)
    clock.clockout_frequency = clock.CLOCKOUT_FREQ_DISABLED
    print(f"clock-pulses: {counter.count}")
    print(f"clock-freq:   {counter.count/DURATION}")
