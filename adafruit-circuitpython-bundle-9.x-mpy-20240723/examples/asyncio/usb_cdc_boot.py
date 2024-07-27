# SPDX-FileCopyrightText: 2022 Phil Underwood
#
# SPDX-License-Identifier: Unlicense
"""
Save this file as boot.py on CIRCUITPY to enable the usb_cdc.data serial device
"""
import usb_cdc

usb_cdc.enable(data=True, console=True)
