# SPDX-FileCopyrightText: Copyright (c) 2023 Liz Clark for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_wii_classic

i2c = board.STEMMA_I2C()
ctrl_pad = adafruit_wii_classic.Wii_Classic(i2c)

while True:
    left_x, left_y = ctrl_pad.joystick_l
    right_x, right_y = ctrl_pad.joystick_r
    left_pressure = ctrl_pad.l_shoulder.LEFT_FORCE
    right_pressure = ctrl_pad.r_shoulder.RIGHT_FORCE
    print("joystick_l = {},{}".format(left_x, left_y))
    print("joystick_r = {},{}".format(right_x, left_y))
    print("left shoulder = {}".format(left_pressure))
    print("right shoulder = {}".format(right_pressure))
    if ctrl_pad.buttons.A:
        print("button A")
    if ctrl_pad.buttons.B:
        print("button B")
    if ctrl_pad.d_pad.UP:
        print("dpad Up")
    if ctrl_pad.d_pad.DOWN:
        print("dpad Down")
    if ctrl_pad.d_pad.LEFT:
        print("dpad Left")
    if ctrl_pad.d_pad.RIGHT:
        print("dpad Right")
    time.sleep(0.5)
