# SPDX-FileCopyrightText: Copyright (c) 2021 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import board
import digitalio
import rotaryio
import usb_hid

from adafruit_debouncer import Debouncer
import adafruit_radial_controller

switch = digitalio.DigitalInOut(board.SWITCH)
switch.pull = digitalio.Pull.DOWN
debounced_switch = Debouncer(switch)

encoder = rotaryio.IncrementalEncoder(board.ROTA, board.ROTB)

radial_controller = adafruit_radial_controller.RadialController(usb_hid.devices)

last_position = 0
DEGREE_TENTHS_MULTIPLIER = 100

while True:
    debounced_switch.update()
    if debounced_switch.rose:
        radial_controller.press()
    if debounced_switch.fell:
        radial_controller.release()

    position = encoder.position
    delta = position - last_position
    if delta != 0:
        radial_controller.rotate(delta * DEGREE_TENTHS_MULTIPLIER)
        last_position = position
