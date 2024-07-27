# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit

kit = MotorKit(i2c=board.I2C())

kit.stepper1.release()

while True:
    print("Single coil steps")
    for i in range(100):
        kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
    for i in range(100):
        kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)

    print("Double coil steps")
    for i in range(100):
        kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
    for i in range(100):
        kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)

    print("Interleaved coil steps")
    for i in range(100):
        kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.INTERLEAVE)
    for i in range(100):
        kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)

    print("Microsteps")
    for i in range(100):
        kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.MICROSTEP)
    for i in range(100):
        kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.MICROSTEP)
