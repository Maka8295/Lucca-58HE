# SPDX-FileCopyrightText: Copyright (c) 2022 Liz Clark for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time
import board
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
from adafruit_tca8418 import TCA8418

displayio.release_displays()

oled_reset = board.D1

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
tca = TCA8418(i2c)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3D, reset=oled_reset)

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

#  display width and height setup
WIDTH = 128
HEIGHT = 64
BORDER = 5

#  display setup
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

splash = displayio.Group()
display.root_group = splash

# text area setup
title_text = "TCA8418 Demo"
title_area = label.Label(
    terminalio.FONT, text=title_text, color=0xFFFFFF, x=10, y=10 // 2 + 1
)
splash.append(title_area)

key_text = " "
key_area = label.Label(
    terminalio.FONT, text=key_text, color=0xFFFFFF, x=10, y=HEIGHT // 2 + 1
)
splash.append(key_area)

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
                #  print each key pressed to display consecutively
                key_area.text = key_area.text + keymap[col][row]
            else:
                print("Key up")
            #  use row & column coordinates to print key name
            print("Row %d, Column %d, Key %s" % (row, col, keymap[col][row]))
        tca.key_int = True  # clear the IRQ by writing 1 to it
        time.sleep(0.01)
