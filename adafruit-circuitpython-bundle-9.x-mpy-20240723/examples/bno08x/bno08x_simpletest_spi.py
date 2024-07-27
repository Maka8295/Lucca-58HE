# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
from time import sleep
import board
import busio
from digitalio import DigitalInOut, Direction
from adafruit_bno08x.spi import BNO08X_SPI

# need to limit clock to 3Mhz
spi = busio.SPI(board.SCK, MISO=board.MISO, MOSI=board.MOSI)

cs = DigitalInOut(board.D5)
cs.direction = Direction.OUTPUT

int_pin = DigitalInOut(board.D6)
int_pin.direction = Direction.INPUT

wake_pin = DigitalInOut(board.D9)
wake_pin.direction = Direction.INPUT

reset_pin = DigitalInOut(board.D9)
reset_pin.direction = Direction.INPUT

bno = BNO08X_SPI(spi, cs, int_pin, wake_pin, reset_pin, debug=True)

while True:
    print("getting quat")
    quat = bno.quaternion  # pylint:disable=no-member
    print("Rotation Vector Quaternion:")
    print(
        "I: %0.6f  J: %0.6f K: %0.6f  Real: %0.6f" % (quat.i, quat.j, quat.k, quat.real)
    )
    print("")
    sleep(0.5)
