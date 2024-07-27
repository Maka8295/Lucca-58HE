# SPDX-FileCopyrightText: 2023 Bernhard Bablok
# SPDX-License-Identifier: MIT

# Simple demo for timer operation, using the interrupt-pin

import time
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_pcf8523.timer import Timer
from adafruit_pcf8523.clock import Clock

LOW_FREQ_TIMER = 10
HIGH_FREQ_TIMER = 0.02
HIGH_FREQ_TIME = 10
PIN_INT = board.GP5
PIN_SDA = board.GP2
PIN_SCL = board.GP3
# use board.SCL and board.SDA if available

i2c = busio.I2C(PIN_SCL, PIN_SDA)
# or i2c = board.I2C() if available
timer = Timer(i2c)
clock = Clock(timer.i2c_device)
clock.clockout_frequency = clock.CLOCKOUT_FREQ_DISABLED

# interrupt pin
intpin = DigitalInOut(PIN_INT)
intpin.direction = Direction.INPUT
intpin.pull = Pull.UP

# Main loop:
timer.pulsed = False
timer.timer_interrupt = True
while True:
    print("low-frequency timer: checking interrupt")
    timer.timer_enabled = False
    timer.timer_status = False
    timer.timer_frequency = timer.TIMER_FREQ_1HZ
    timer.timer_value = LOW_FREQ_TIMER
    start = time.monotonic()
    timer.timer_enabled = True
    while intpin.value and time.monotonic() - start < LOW_FREQ_TIMER + 1:
        pass
    if intpin.value:
        # shoud not happen!
        print(f"error: timer did not fire within {LOW_FREQ_TIMER+1} seconds!")
    else:
        elapsed = time.monotonic() - start
        print(f"elapsed: {elapsed}")

    print("high-frequency timer: checking interrupt")
    timer.timer_enabled = False
    timer.timer_status = False
    timer.timer_frequency = timer.TIMER_FREQ_4KHZ
    timer.timer_value = min(round(HIGH_FREQ_TIMER * 4096), 255)
    counter = 0
    start = time.monotonic()
    end = start + HIGH_FREQ_TIME
    timer.timer_enabled = True
    while time.monotonic() < end:
        if intpin.value:
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
