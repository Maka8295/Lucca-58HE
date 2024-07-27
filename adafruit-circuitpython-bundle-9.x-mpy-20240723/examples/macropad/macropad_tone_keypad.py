# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
MacroPad tone demo. Plays a different tone for each key pressed and lights up each key a different
color while the key is pressed.
"""
from rainbowio import colorwheel
from adafruit_macropad import MacroPad

macropad = MacroPad()

tones = [196, 220, 246, 262, 294, 330, 349, 392, 440, 494, 523, 587]

while True:
    key_event = macropad.keys.events.get()

    if key_event:
        if key_event.pressed:
            macropad.pixels[key_event.key_number] = colorwheel(
                int(255 / 12) * key_event.key_number
            )
            macropad.start_tone(tones[key_event.key_number])

        else:
            macropad.pixels.fill((0, 0, 0))
            macropad.stop_tone()
