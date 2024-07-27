# SPDX-FileCopyrightText: Copyright (c) 2021 Aaron Pendley
#
# SPDX-License-Identifier: Unlicense
"""
MacroPad extended tone demo. Expands upon the basic tone demo by using
a stack to track pressed keys, allowing multiple keys to be pressed at once,
while preserving the order they were pressed. Also, improved responsiveness by
updating the Neopixels only when one of the key states has changed.
"""

from rainbowio import colorwheel
from adafruit_macropad import MacroPad

macropad = MacroPad()

# We'll show the pixels manually
macropad.pixels.auto_write = False

# Notes for each key
tones = [196, 220, 246, 262, 294, 330, 349, 392, 440, 494, 523, 587]

# When a key is pressed we'll append it to the end, and when a key is
# released we'll remove it. This results in a list of pressed keys in
# the order they were pressed.
key_pressed_stack = []

# When at least one key is pressed, this will
# be the index of the currently playing note.
playing_index = None


# Helper to convert an integer to an rgb value.
def rgb_from_int(rgb):
    blue = rgb & 255
    green = (rgb >> 8) & 255
    red = (rgb >> 16) & 255
    return red, green, blue


# Loop forever, until the heat death of the universe
# (or we lose power, whichever comes first).
while True:
    # To save time, we'll only update the pixels when a key event happens.
    update_pixels = False

    # Process all pending events.
    while macropad.keys.events:
        key_event = macropad.keys.events.get()

        # We need to update the pixels again at the end of the main loop.
        update_pixels = True

        if key_event.pressed:
            # Append pressed key to the end of the stack
            key_pressed_stack.append(key_event.key_number)
        else:
            # Remove released key from the stack
            key_pressed_stack.remove(key_event.key_number)

            # Turn this pixel off since the key is no longer pressed.
            macropad.pixels[key_event.key_number] = 0

    # How many keys are currently pressed?
    pressed_count = len(key_pressed_stack)

    # There are some keys pressed.
    if pressed_count > 0:
        # Get the most recently pressed key
        top_index = key_pressed_stack[pressed_count - 1]

        # If the most recently pressed key's tone isn't already playing;
        if top_index != playing_index:
            # If a tone was playing, stop it, so we can play the next one.
            if playing_index is not None:
                macropad.stop_tone()

            # Play this key's tone and remember which one it is.
            macropad.start_tone(tones[top_index])
            playing_index = top_index

    # There are no keys pressed.
    else:
        # If a tone was playing, stop it.
        if playing_index is not None:
            macropad.stop_tone()
            playing_index = None

    # If a key was pressed or released, update the pixels for the pressed keys.
    if update_pixels:
        for key_index in key_pressed_stack:
            # Get the color for this key.
            wheel_color = colorwheel(int(255 / 12) * key_index)

            if key_index == playing_index:
                # Show the currently playing key at full brightness.
                macropad.pixels[key_index] = wheel_color
            else:
                # Dim the rest of the keys to 10% brightness.
                (r, g, b) = rgb_from_int(wheel_color)
                macropad.pixels[key_index] = (r * 0.1, g * 0.1, b * 0.1)

        # Don't forget to show the pixels!
        macropad.pixels.show()
