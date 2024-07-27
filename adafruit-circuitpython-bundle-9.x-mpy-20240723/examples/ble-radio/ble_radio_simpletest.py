# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This demo uses the adafruit_radio module to send and receive messages.
Devices are switched between broadcast and scanning using the slide switch.
The buttons change the message to be sent.
"""
import digitalio
import board
from adafruit_ble_radio import Radio


slide_switch = digitalio.DigitalInOut(board.SLIDE_SWITCH)
slide_switch.pull = digitalio.Pull.UP
button_a = digitalio.DigitalInOut(board.BUTTON_A)
button_a.pull = digitalio.Pull.DOWN
button_b = digitalio.DigitalInOut(board.BUTTON_B)
button_b.pull = digitalio.Pull.DOWN

led = digitalio.DigitalInOut(board.D13)
led.switch_to_output()

msg = [
    "hello",
    "hi",
    "foo",
    "bar",
    "baz",
]

i = 0
r = Radio()

while True:
    if slide_switch.value:
        print("Sending messages...")
        while slide_switch.value:
            last_i = i
            if button_a.value:
                i += 1
            if button_b.value:
                i -= 1
            i %= len(msg)
            m = msg[i]
            print("Sending {}".format(m))
            r.send(m)
            # Alternative
            # r.send_bytes(b"Arbitrary bytes")
    else:
        print("Scanning for messages...")
        while not slide_switch.value:
            m = r.receive_full()
            if m:
                print("Received message: {}".format(m))
            # Alternative
            # m = r.receive()
            # if m:
            #    print(m)
