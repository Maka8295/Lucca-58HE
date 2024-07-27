# SPDX-FileCopyrightText: Copyright (c) 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
International layout demo for MacroPad.
"""
import time
from keyboard_layout_win_fr import KeyboardLayout
from keycode_win_fr import Keycode
from adafruit_macropad import MacroPad

macropad = MacroPad(
    layout_class=KeyboardLayout,
    keycode_class=Keycode,
)

keycodes = [
    "https://adafruit.com/",
    "https://adafru.it/discord",
    "https://circuitpython.org",
    Keycode.A,
    Keycode.D,
    Keycode.A,
    Keycode.F,
    Keycode.R,
    Keycode.U,
    Keycode.I,
    Keycode.T,
    Keycode.PERIOD,
    #    Keycode.C, Keycode.O, Keycode.M,
]

while True:
    key_event = macropad.keys.events.get()
    if key_event:
        keycode = keycodes[key_event.key_number]
        if key_event.pressed:
            if isinstance(keycode, int):
                macropad.keyboard.press(keycode)
            else:
                macropad.keyboard_layout.write(keycode)
        else:
            if isinstance(keycode, int):
                macropad.keyboard.release(keycode)
    time.sleep(0.05)
