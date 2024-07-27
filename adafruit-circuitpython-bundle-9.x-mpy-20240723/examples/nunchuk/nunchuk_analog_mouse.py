# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import usb_hid
from adafruit_hid.mouse import Mouse
import adafruit_nunchuk

m = Mouse(usb_hid.devices)
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
nc = adafruit_nunchuk.Nunchuk(i2c)

centerX = 128
centerY = 128

scaleX = 0.3
scaleY = 0.3

cDown = False
zDown = False

# This is to allow double checking (only on left click - and it doesn't really work)
CHECK_COUNT = 0


# This is just to show that we're getting back data - uncomment it and hold down the buttons
# while True:
#    print((0 if nc.button_C else 1, 0 if nc.button_Z else 1))

while True:
    x, y = nc.joystick
    # Eliminate spurious reads
    if x == 255 or y == 255:
        continue
    relX = x - centerX
    relY = centerY - y

    m.move(int(scaleX * relX), int(scaleY * relY), 0)

    buttons = nc.buttons
    c = buttons.C
    z = buttons.Z

    if z and not zDown:
        stillDown = True
        for n in range(CHECK_COUNT):
            if nc.button_Z:
                stillDown = False
                break
        if stillDown:
            m.press(Mouse.LEFT_BUTTON)
            zDown = True
    elif not z and zDown:
        stillDown = True
        for n in range(CHECK_COUNT):
            if not nc.button_Z:
                stillDown = False
                break
        if stillDown:
            m.release(Mouse.LEFT_BUTTON)
            zDown = False
    if c and not cDown:
        m.press(Mouse.RIGHT_BUTTON)
        cDown = True
    elif not c and cDown:
        m.release(Mouse.RIGHT_BUTTON)
        cDown = False
