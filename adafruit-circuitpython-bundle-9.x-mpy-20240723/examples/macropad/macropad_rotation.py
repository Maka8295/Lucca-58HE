# SPDX-FileCopyrightText: Copyright (c) 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
MacroPad rotation demo. Rotates the display 90 degrees and remaps the NeoPixels and keys to match.
Lights up the associated pixel when the key is pressed. Displays the key number pressed and the
rotary encoder relative position on the display.
"""
from rainbowio import colorwheel
from adafruit_macropad import MacroPad

macropad = MacroPad(rotation=90)

text_lines = macropad.display_text(title="MacroPad \nInfo")

while True:
    key_event = macropad.keys.events.get()
    if key_event:
        if key_event.pressed:
            text_lines[1].text = "Key {}!".format(key_event.key_number)
            macropad.pixels[key_event.key_number] = colorwheel(
                int(255 / 12) * key_event.key_number
            )
        else:
            macropad.pixels.fill((0, 0, 0))
    text_lines[2].text = "Encoder {}".format(macropad.encoder)
    text_lines.show()
