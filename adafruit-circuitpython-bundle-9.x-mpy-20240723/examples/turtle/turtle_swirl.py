# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
from adafruit_turtle import turtle, Color

turtle = turtle(board.DISPLAY)


turtle.pendown()

colors = [Color.ORANGE, Color.PURPLE]

for x in range(400):
    turtle.pencolor(colors[x % 2])
    turtle.forward(x)
    turtle.left(91)

while True:
    pass
