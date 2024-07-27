# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

# On an Adafruit Floppsy, Adafruit Feather M4 or Adafruit Feather RP2040 with
# Floppy Featherwing, print the root directory listing of a 1.44MB floppy

# Leave this line here, this memory must be allocated as early as possible to avoid
# memory fragmentation
flux_buffer = bytearray(110000)

# pylint: disable=wrong-import-position
import os
import storage
import board
import adafruit_datetime as datetime
import adafruit_floppy

epoch = datetime.datetime(1970, 1, 1)

ST_SIZE = 6
ST_TIME = 7
SV_BFREE = 3

if hasattr(board, "DENSITY"):  # floppsy
    floppy = adafruit_floppy.Floppy(
        densitypin=board.DENSITY,
        indexpin=board.INDEX,
        selectpin=board.SELECT,
        motorpin=board.MOTOR,
        directionpin=board.DIRECTION,
        steppin=board.STEP,
        track0pin=board.TRACK0,
        protectpin=board.WRPROT,
        rddatapin=board.RDDATA,
        sidepin=board.SIDE,
        readypin=board.READY,
        floppydirectionpin=board.FLOPPY_DIRECTION,
    )

else:
    D24 = getattr(board, "D24") or getattr(board, "A4")
    D25 = getattr(board, "D25") or getattr(board, "A5")

    floppy = adafruit_floppy.Floppy(
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
        flux_buffer=flux_buffer,
    )

floppy.find_track0()

f = adafruit_floppy.FloppyBlockDevice(floppy, sectors=18, flux_buffer=flux_buffer)

vfs = storage.VfsFat(f)
storage.mount(vfs, "/floppy")

print(f"floppy mounted, Capacity {f.count()} blocks")
print()

print("Directory listing")
for i, f in enumerate(sorted(os.listdir("/floppy"))):
    st = os.stat("/floppy/" + f)
    d = epoch + datetime.timedelta(seconds=st[ST_TIME])
    print(f"{f:12} {st[ST_SIZE]:6} bytes, {d}")

sv = os.statvfs("/floppy")
print(f"{sv[SV_BFREE]*512} bytes free")
