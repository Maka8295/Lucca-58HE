# SPDX-FileCopyrightText: 2023 Bernhard Bablok
# SPDX-License-Identifier: MIT

# Simple demo for timer operation using the timer-flag

import time
import board
import busio
from adafruit_pcf8523.timer import Timer
from adafruit_pcf8523.clock import Clock

LOW_FREQ_TIMER = 10
HIGH_FREQ_TIMER = 0.02
HIGH_FREQ_TIME = 10
PIN_SDA = board.GP2
PIN_SCL = board.GP3
# use board.SCL and board.SDA if available

i2c = busio.I2C(PIN_SCL, PIN_SDA)
# or i2c = board.I2C() if available
timer = Timer(i2c)
clock = Clock(timer.i2c_device)
clock.clockout_frequency = clock.CLOCKOUT_FREQ_DISABLED

# Main loop:
while True:
    print("low-frequency timer: checking timer-flag")
    timer.timer_enabled = False
    timer.timer_status = False
    timer.timer_frequency = timer.TIMER_FREQ_1HZ
    timer.timer_value = LOW_FREQ_TIMER
    start = time.monotonic()
    timer.timer_enabled = True
    while not timer.timer_status and time.monotonic() - start < LOW_FREQ_TIMER + 1:
        pass
    if not timer.timer_status:
        # shoud not happen!
        print(f"error: timer did not fire within {LOW_FREQ_TIMER+1} seconds!")
    else:
        elapsed = time.monotonic() - start
        print(f"elapsed: {elapsed}")

    print("high-frequency timer: checking timer-flag")
    timer.timer_enabled = False
    timer.timer_status = False
    timer.timer_frequency = timer.TIMER_FREQ_4KHZ
    timer.timer_value = min(round(HIGH_FREQ_TIMER * 4096), 255)
    counter = 0
    start = time.monotonic()
    end = start + HIGH_FREQ_TIME
    timer.timer_enabled = True
    while time.monotonic() < end:
        if not timer.timer_status:
            continue
        timer.timer_status = False
        counter += 1
    if counter > 0:
        mean_interval = (time.monotonic() - start) / counter
        print(f"interval requested: {HIGH_FREQ_TIMER}")
        print(f"interval observed:  {mean_interval} (mean of {counter} alarms)")
    else:
        print(f"error: timer did not fire within {HIGH_FREQ_TIME} seconds!")
        print("error: timer did not fire")
