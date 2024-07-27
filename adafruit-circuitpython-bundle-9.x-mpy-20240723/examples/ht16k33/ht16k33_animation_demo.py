# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
    Test script for display animations on an HT16K33 with alphanumeric display

    The display must be initialized with auto_write=False.
"""

from time import sleep
import board
from adafruit_ht16k33.segments import Seg14x4
from adafruit_ht16k33.animations import Animation

#   Initialize the I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
display = Seg14x4(i2c, auto_write=False)
#   Brightness of the display (0.0 to 1.0)
display.brightness = 0.3

ani = Animation(display)

try:
    text = "Init"

    display.fill(1)
    display.show()
    sleep(1)
    display.fill(0)
    display.show()

    display.print(text)
    display.show()
    sleep(2)
    display.fill(0)
    display.show()
    sleep(1)

    ani.count_down()
    sleep(0.2)

    text = "Go!!"

    display.print(text)
    display.show()
    sleep(1.5)
    display.fill(0)
    display.show()
    sleep(0.5)
    print()

    while True:
        #   Arrow
        print("Arrow")
        ani.animate([0, 1, 2], [192], 0.1)
        ani.animate([3], [2368], 0.1)
        sleep(1.0)
        display.fill(0)
        sleep(1.0)

        #   Flying
        print("Flying")
        cyc = 0

        while cyc < 5:
            ani.animate([0], [1280, 192, 10240, 192], 0.2)

            cyc += 1

        ani.animate([0], [0])
        sleep(1.0)
        display.fill(0)
        sleep(1.0)

        #   Chase forward and reverse.
        print("Chase forward and reverse")
        ani.chase_forward_and_reverse(0.01, 5)
        sleep(1.0)
        display.fill(0)
        sleep(1.0)

        #   Testing writing to more than one segment simultaneously
        print("Prelude to Spinners")
        ani.prelude_to_spinners(0.1, 5)
        sleep(1.0)
        display.fill(0)
        display.show()
        sleep(1.0)

        print("Spinners")
        ani.spinners(0.1, 20)
        sleep(1.0)
        display.fill(0)
        display.show()
        sleep(1.0)

        print("Enclosed Spinners")
        ani.enclosed_spinners(0.1, 20)
        sleep(1.0)
        display.fill(0)
        display.show()
        sleep(1.0)

        print()
except KeyboardInterrupt:
    display.fill(0)
    display.show()
