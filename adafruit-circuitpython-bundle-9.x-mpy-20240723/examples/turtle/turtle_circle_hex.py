# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
from adafruit_turtle import turtle

turtle = turtle(board.DISPLAY)
turtle.pendown()

for _ in range(32):
    turtle.circle(50, steps=6)
    turtle.right(11.1111)

while True:
    pass
