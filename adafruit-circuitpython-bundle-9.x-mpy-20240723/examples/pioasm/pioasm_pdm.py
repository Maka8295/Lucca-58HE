# SPDX-FileCopyrightText: 2021 Scott Shawcroft, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import array
import time
import board
import digitalio
import rp2pio
import adafruit_pioasm

trigger = digitalio.DigitalInOut(board.D4)
trigger.switch_to_output(True)

# signed 16 bit
s16 = array.array("H", [0] * 10000)

# Capturing on the rising edge is the left PDM channel. To do right, swap the
# side set values.
#
# push iffull means it'll push every 32 bits and noop otherwise. noblock causes
# data to be dropped instead of stopping the clock. This allows the mic to warm
# up before the readinto.
program = """
.program pdmin
.side_set 1
    in pins 1            side 0b1
    push iffull noblock  side 0b0
"""

assembled = adafruit_pioasm.assemble(program)

sm = rp2pio.StateMachine(
    assembled,
    frequency=24000 * 2 * 32,
    first_in_pin=board.D12,
    first_sideset_pin=board.D11,
    auto_push=False,
    in_shift_right=True,
    push_threshold=32,
)

# Give the mic a bit of time to warm up (thanks to our noblock.)
time.sleep(0.1)

print("starting read")
trigger.value = False
# Clear the fifo to ignore old values and reset rxstall.
sm.clear_rxfifo()
sm.readinto(s16)
# Capture rxstall quickly so we can hopefully tell if we dropped data. (We
# definitely will at some point after readinto is done.)
stalled = sm.rxstall
trigger.value = True
print("read done")

if stalled:
    print("missed samples")

# These are raw one bit samples. audiobusio.PDMIn does an extra filtering step.
# for v in s16:
#     print(v)

print("done")
