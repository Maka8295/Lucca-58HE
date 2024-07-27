# SPDX-FileCopyrightText: 2020 Foamyguy, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""
CircuitPython example for Monster M4sk.

Draws a basic eye dot on each screen. Looks at nose
when booped. Prints acceleration and light sensor
data when booped as well.
"""
import time
import board
import displayio
from adafruit_display_shapes.circle import Circle
import adafruit_monsterm4sk


# Account for slight screen difference if you want
LEFT_Y_OFFSET = 0  # 12 # my left screen is a tad higher

SCREEN_SIZE = 240

i2c_bus = board.I2C()  # uses board.SCL and board.SDA
# i2c_bus = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

mask = adafruit_monsterm4sk.MonsterM4sk(i2c=i2c_bus)

left_group = displayio.Group()
mask.left_display.root_group = left_group

right_group = displayio.Group()
mask.right_display.root_group = right_group

right_circle = Circle(SCREEN_SIZE // 2, SCREEN_SIZE // 2, 40, fill=0x0000FF)
right_group.append(right_circle)

left_circle = Circle(SCREEN_SIZE // 2, SCREEN_SIZE // 2, 40, fill=0x00AA66)
left_group.append(left_circle)

while True:
    # print(mask.boop)
    if mask.boop:
        left_circle.x = 0
        right_circle.x = SCREEN_SIZE - 40 - 40 - 2

        right_circle.y = SCREEN_SIZE // 4 - 40
        left_circle.y = SCREEN_SIZE // 4 - 40 + LEFT_Y_OFFSET
        print(mask.acceleration)
        print(mask.light)
        time.sleep(0.5)
    else:
        left_circle.x = SCREEN_SIZE // 2 - 40
        right_circle.x = SCREEN_SIZE // 2 - 40

        right_circle.y = SCREEN_SIZE // 2 - 40
        left_circle.y = SCREEN_SIZE // 2 - 40 + LEFT_Y_OFFSET
