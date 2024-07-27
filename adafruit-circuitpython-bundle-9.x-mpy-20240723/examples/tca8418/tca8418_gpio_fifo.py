# SPDX-FileCopyrightText: Copyright (c) 2022 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time
import board
from adafruit_debug_i2c import DebugI2C
from adafruit_tca8418 import TCA8418

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

debug_i2c = DebugI2C(i2c)

tca = TCA8418(i2c)

# set up all R pins and some of the C pins as GPIO pins
INPINS = (
    TCA8418.R0,
    TCA8418.R1,
    TCA8418.R2,
    TCA8418.R3,
    TCA8418.R4,
    TCA8418.R5,
    TCA8418.R6,
    TCA8418.R7,
    TCA8418.C0,
    TCA8418.C1,
    TCA8418.C2,
    TCA8418.C3,
)

# make them inputs with pullups
for pin in INPINS:
    tca.gpio_mode[pin] = True
    tca.gpio_direction[pin] = False
    tca.pullup[pin] = True

    # make sure the key pins generate FIFO events
    tca.enable_int[pin] = True
    # we will stick events into the FIFO queue
    tca.event_mode_fifo[pin] = True

# turn on INT output pin, note we're using the GPIO as key events
# so we want to enable the *key event* interrupt!
tca.key_intenable = True


while True:
    if tca.gpi_int:
        # first figure out how big the queue is
        events = tca.events_count
        # now print each event in the queue
        for _ in range(events):
            keyevent = tca.next_event
            print(
                "\tKey event: 0x%02X - GPIO #%d " % (keyevent, (keyevent & 0xF) - 1),
                end="",
            )
            if keyevent & 0x80:
                print("key down")
            else:
                print("key up")
        tca.gpi_int = True  # clear the IRQ by writing 1 to it
        time.sleep(0.01)
