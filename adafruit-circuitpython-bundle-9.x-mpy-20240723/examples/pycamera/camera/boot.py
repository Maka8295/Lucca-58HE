# SPDX-FileCopyrightText: 2023 Jeff Epler for Adafruit Industries
# SPDX-FileCopyrightText: 2023 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""Automatically create the /sd mount point at boot time"""

import os
import storage

storage.remount("/", readonly=False)

try:
    os.mkdir("/sd")
except OSError:
    pass  # It's probably 'file exists', OK to ignore

storage.remount("/", readonly=True)
