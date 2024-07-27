# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
# SPDX-License-Identifier: MIT
from time import sleep
import board
from adafruit_as7341 import AS7341

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = AS7341(i2c)


def bar_graph(read_value):
    scaled = int(read_value / 1000)
    return "[%5d] " % read_value + (scaled * "*")


while True:
    sensor_channels = sensor.all_channels
    print("F1 - 415nm/Violet  %s" % bar_graph(sensor_channels[0]))
    print("F2 - 445nm//Indigo %s" % bar_graph(sensor_channels[1]))
    print("F3 - 480nm//Blue   %s" % bar_graph(sensor_channels[2]))
    print("F4 - 515nm//Cyan   %s" % bar_graph(sensor_channels[3]))
    print("F5 - 555nm/Green   %s" % bar_graph(sensor_channels[4]))
    print("F6 - 590nm/Yellow  %s" % bar_graph(sensor_channels[5]))
    print("F7 - 630nm/Orange  %s" % bar_graph(sensor_channels[6]))
    print("F8 - 680nm/Red     %s" % bar_graph(sensor_channels[7]))
    print("\n------------------------------------------------")

    sleep(1)
