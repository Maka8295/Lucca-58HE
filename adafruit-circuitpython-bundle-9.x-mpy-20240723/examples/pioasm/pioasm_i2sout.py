# SPDX-FileCopyrightText: 2021 Scott Shawcroft, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import array
import math
import time
import board
import digitalio
import rp2pio
import adafruit_pioasm

trigger = digitalio.DigitalInOut(board.D4)
trigger.switch_to_output(True)

# Generate one period of sine wav.
length = 8000 // 440

# signed 16 bit
s16 = array.array("h", [0] * length)
for i in range(length):
    s16[i] = int(math.sin(math.pi * 2 * i / length) * (2**15))
    print(s16[i])

program = """
.program i2s_with_hold
.side_set 2

; Load the next set of samples
                    ;        /--- LRCLK
                    ;        |/-- BCLK
                    ;        ||
    pull noblock      side 0b01 ; Loads OSR with the next FIFO value or X
    mov x osr         side 0b01 ; Save the new value in case we need it again

    set y 14          side 0b01
bitloop1:
    out pins 1        side 0b10 [2]
    jmp y-- bitloop1  side 0b11 [2]
    out pins 1        side 0b10 [2]

    set y 14          side 0b11 [2]
bitloop0:
    out pins 1        side 0b00 [2]
    jmp y-- bitloop0  side 0b01 [2]
    out pins 1        side 0b00 [2]
"""

assembled = adafruit_pioasm.assemble(program)

dac = rp2pio.StateMachine(
    assembled,
    frequency=800000 * 6,
    first_out_pin=board.D12,
    first_sideset_pin=board.D10,
    sideset_pin_count=2,
    auto_pull=False,
    out_shift_right=False,
    pull_threshold=32,
    wait_for_txstall=False,
)

trigger.value = False
dac.write(s16)
time.sleep(1)
dac.stop()
trigger.value = True

print("done")
