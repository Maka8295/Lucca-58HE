# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

# On an Adafruit Feather M4 or Adafruit Feather RP2040 with Floppy Featherwing,
# do some track-to-track seeking and flux reading.

import board
import adafruit_floppy

D24 = getattr(board, "D24") or getattr(board, "A4")
D25 = getattr(board, "D25") or getattr(board, "A5")

floppy = adafruit_floppy.MFMFloppy(
    densitypin=board.A1,
    indexpin=D25,
    selectpin=board.A0,
    motorpin=board.A2,
    directionpin=board.A3,
    steppin=D24,
    track0pin=board.D10,
    protectpin=board.D11,
    rddatapin=board.D9,
    sidepin=board.D6,
    readypin=board.D5,
)

floppy.selected = True
floppy.spin = True
print("Seek track 8")
floppy.track = 8
print("Seek track 0")
floppy.track = 0
print("Read partial track raw flux data")
buf = bytearray(30000)
n_read = floppy.flux_readinto(buf)
print("read", n_read)
buckets = [0] * 256
for b in buf:
    buckets[b] += 1
oi = -1
for i, bi in enumerate(buckets):
    if bi > 10:
        if i != oi + 1:
            print("---")
        oi = i
        print(f"{i:3} {bi:5}")
