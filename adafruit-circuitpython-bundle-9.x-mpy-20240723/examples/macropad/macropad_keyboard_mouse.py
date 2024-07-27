# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
MacroPad HID keyboard and mouse demo. The demo sends "a" when the first key is pressed, a "B" when
the second key is pressed, "Hello, World!" when the third key is pressed, and decreases the volume
when the fourth key is pressed. It sends a right mouse click when the rotary encoder switch is
pressed. Finally, it moves the mouse left and right when the rotary encoder is rotated
counterclockwise and clockwise respectively.
"""
from adafruit_macropad import MacroPad

macropad = MacroPad()

last_position = 0
while True:
    key_event = macropad.keys.events.get()

    if key_event:
        if key_event.pressed:
            if key_event.key_number == 0:
                macropad.keyboard.send(macropad.Keycode.A)
            if key_event.key_number == 1:
                macropad.keyboard.press(macropad.Keycode.SHIFT, macropad.Keycode.B)
                macropad.keyboard.release_all()
            if key_event.key_number == 2:
                macropad.keyboard_layout.write("Hello, World!")
            if key_event.key_number == 3:
                macropad.consumer_control.send(
                    macropad.ConsumerControlCode.VOLUME_DECREMENT
                )

    macropad.encoder_switch_debounced.update()

    if macropad.encoder_switch_debounced.pressed:
        macropad.mouse.click(macropad.Mouse.RIGHT_BUTTON)

    current_position = macropad.encoder

    if macropad.encoder > last_position:
        macropad.mouse.move(x=+5)
        last_position = current_position

    if macropad.encoder < last_position:
        macropad.mouse.move(x=-5)
        last_position = current_position
