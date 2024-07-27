# SPDX-FileCopyrightText: Copyright (c) 2022 Liz Clark for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time
import board
from adafruit_tca8418 import TCA8418

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
tca = TCA8418(i2c)

keymap = (("*", "0", "#"), ("7", "8", "9"), ("4", "5", "6"), ("1", "2", "3"))

# set up all R0-R2 pins and C0-C3 pins as keypads
KEYPADPINS = (
    TCA8418.R0,
    TCA8418.R1,
    TCA8418.R2,
    TCA8418.C0,
    TCA8418.C1,
    TCA8418.C2,
    TCA8418.C3,
)

# make them inputs with pullups
for pin in KEYPADPINS:
    tca.keypad_mode[pin] = True
    # make sure the key pins generate FIFO events
    tca.enable_int[pin] = True
    # we will stick events into the FIFO queue
    tca.event_mode_fifo[pin] = True

# turn on INT output pin
tca.key_intenable = True

while True:
    if tca.key_int:
        # first figure out how big the queue is
        events = tca.events_count
        # now print keyevent, row, column & key name
        for _ in range(events):
            keyevent = tca.next_event
            #  strip keyevent
            event = keyevent & 0x7F
            event -= 1
            #  figure out row
            row = event // 10
            #  figure out column
            col = event % 10
            #  print event type first
            if keyevent & 0x80:
                print("Key down")
            else:
                print("Key up")
            #  use row & column coordinates to print key name
            print("Row %d, Column %d, Key %s" % (row, col, keymap[col][row]))
        tca.key_int = True  # clear the IRQ by writing 1 to it
        time.sleep(0.01)
