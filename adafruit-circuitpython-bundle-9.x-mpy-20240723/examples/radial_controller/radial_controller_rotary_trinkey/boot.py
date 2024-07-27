# SPDX-FileCopyrightText: Copyright (c) 2021 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import usb_hid

import adafruit_radial_controller.device

REPORT_ID = 5

radial_controller_device = adafruit_radial_controller.device.device(REPORT_ID)
usb_hid.enable((radial_controller_device,))
