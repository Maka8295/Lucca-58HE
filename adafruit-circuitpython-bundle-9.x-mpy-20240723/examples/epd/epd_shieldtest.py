# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# EInk Shield test
import time
import digitalio
import busio
import board
from analogio import AnalogIn
from adafruit_epd.epd import Adafruit_EPD
from adafruit_epd.il91874 import Adafruit_IL91874

# create the spi device and pins we will need
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = digitalio.DigitalInOut(board.D10)
dc = digitalio.DigitalInOut(board.D9)
srcs = digitalio.DigitalInOut(board.D8)  # can be None to use internal memory

# give them all to our driver
print("Creating display")
display = Adafruit_IL91874(
    176,
    264,
    spi,  # 2.7" Tri-color display
    cs_pin=ecs,
    dc_pin=dc,
    sramcs_pin=srcs,
    rst_pin=None,
    busy_pin=None,
)

display.rotation = 1


def read_buttons():
    with AnalogIn(board.A3) as ain:
        reading = ain.value / 65535
        if reading > 0.75:
            return None
        if reading > 0.4:
            return 4
        if reading > 0.25:
            return 3
        if reading > 0.13:
            return 2
        return 1


while True:
    button = read_buttons()
    if not button:
        continue
    print("Button #%d pressed" % button)
    if button == 1:
        print("Clear buffer")
        display.fill(Adafruit_EPD.WHITE)
        display.display()
    if button == 2:
        print("Draw Rectangles")
        display.fill_rect(5, 5, 10, 10, Adafruit_EPD.RED)
        display.rect(0, 0, 20, 30, Adafruit_EPD.BLACK)
        display.display()
    if button == 3:
        print("Draw lines")
        display.line(0, 0, display.width - 1, display.height - 1, Adafruit_EPD.BLACK)
        display.line(0, display.height - 1, display.width - 1, 0, Adafruit_EPD.RED)
        display.display()
    if button == 4:
        print("Draw text")
        display.text("hello world", 25, 10, Adafruit_EPD.BLACK)
        display.display()
    time.sleep(0.01)
