# SPDX-FileCopyrightText: 2022 Jeff Epler, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Demonstrate background writing, including loop writing, with morse code.

On any rp2040 board with board.LED, this will alternately send 'SOS' and 'TEST'
via the LED, demonstrating that Python code continues to run while the morse
code data is transmitted. Alternately, change one line below to make it send
'TEST' forever in a loop, again while Python code continues to run.

The combination of "LED status" and duration is sent to the PIO as 16-bit number:
The top bit is 1 if the LED is turned on and 0 otherwise.  The other 15 bits form a delay
value from 1 to 32767. A subset of the morse code 'alphabit' is created, with everthing
based on the 'DIT duration' of about 128ms (1MHz / 32 / 4000).

https://en.wikipedia.org/wiki/Morse_code
"""

import array
import time
from board import LED
from rp2pio import StateMachine
from adafruit_pioasm import Program

# This program turns the LED on or off depending on the first bit of the value,
# then delays a length of time given by the next 15 bits of the value.
# By correctly choosing the durations, a message in morse code can be sent.
pio_code = Program(
    """
        out x, 1
        mov pins, x
        out x, 15
    busy_wait:
        jmp x--, busy_wait [31]
        """
)


# The top bit of the command is the LED value, on or off
LED_ON = 0x8000
LED_OFF = 0x0000

# The other 15 bits are a delay duration.
# It must be the case that 4 * DIT_DURATION < 32768
DIT_DURATION = 4000
DAH_DURATION = 3 * DIT_DURATION

# Build up some elements of morse code, based on the wikipedia article.
DIT = array.array("H", [LED_ON | DIT_DURATION, LED_OFF | DIT_DURATION])
DAH = array.array("H", [LED_ON | DAH_DURATION, LED_OFF | DIT_DURATION])
# That is, two more DAH-length gaps for a total of three
LETTER_SPACE = array.array("H", [LED_OFF | (2 * DAH_DURATION)])
# That is, four more DAH-length gaps (after a letter space) for a total of seven
WORD_SPACE = array.array("H", [LED_OFF | (4 * DIT_DURATION)])

# Letters and words can be created by concatenating ("+") the elements
E = DIT + LETTER_SPACE
O = DAH + DAH + DAH + LETTER_SPACE
S = DIT + DIT + DIT + LETTER_SPACE
T = DAH + LETTER_SPACE
SOS = S + O + S + WORD_SPACE
TEST = T + E + S + T + WORD_SPACE

sm = StateMachine(
    pio_code.assembled,
    frequency=1_000_000,
    first_out_pin=LED,
    pull_threshold=16,
    auto_pull=True,
    out_shift_right=False,
    **pio_code.pio_kwargs,
)

# To simply repeat 'TEST' forever, change to 'if True':
if False:  # pylint: disable=using-constant-test
    print("Sending out TEST forever", end="")
    sm.background_write(loop=TEST)
    while True:
        print(end=".")
        time.sleep(0.1)

# But instead, let's alternate SOS and TEST, forever:

while True:
    for plain, morse in (
        ("SOS", SOS),
        ("TEST", TEST),
    ):
        print(f"Sending out {plain}", end="")
        sm.background_write(morse)
        sm.clear_txstall()
        while not sm.txstall:
            print(end=".")
            time.sleep(0.1)
        print()
        print("Message all sent to StateMachine (including emptying FIFO)")
        print()
