# SPDX-FileCopyrightText: Copyright (c) 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
Simpletest demo for MacroPad. Prints the key pressed, the relative position of the rotary
encoder, and the state of the rotary encoder switch to the serial console.
"""
import time
from adafruit_macropad import MacroPad

macropad = MacroPad()

while True:
    key_event = macropad.keys.events.get()
    if key_event and key_event.pressed:
        print("Key pressed: {}".format(key_event.key_number))
    print("Encoder: {}".format(macropad.encoder))
    print("Encoder switch: {}".format(macropad.encoder_switch))
    time.sleep(0.4)
