# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
from adafruit_turtle import turtle

turtle = turtle(board.DISPLAY)


# turtle.penup()
# turtle.right(45)
# turtle.forward(90)
# turtle.right(75)

turtle.pendown()
for _ in range(21):
    for _ in range(6):
        turtle.forward(50)
        turtle.right(61)
    turtle.right(11.1111)

while True:
    pass
