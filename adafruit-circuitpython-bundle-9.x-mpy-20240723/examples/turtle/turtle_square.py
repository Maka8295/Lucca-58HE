# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
from adafruit_turtle import Color, turtle

turtle = turtle(board.DISPLAY)
print("Turtle time! Lets draw a simple square")

turtle.pencolor(Color.WHITE)
turtle.pendown()

for _ in range(4):
    turtle.forward(25)
    turtle.left(90)

while True:
    pass
