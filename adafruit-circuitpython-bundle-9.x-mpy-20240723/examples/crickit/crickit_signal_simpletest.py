# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Crickit library demo - Signal terminals

from adafruit_crickit import crickit

# Write Signal terminal 1 and read Signal terminal 2.

ss = crickit.seesaw

ss.pin_mode(crickit.SIGNAL1, ss.OUTPUT)
ss.pin_mode(crickit.SIGNAL2, ss.INPUT)

ss.digital_write(crickit.SIGNAL1, True)
print(ss.digital_read(crickit.SIGNAL2))
