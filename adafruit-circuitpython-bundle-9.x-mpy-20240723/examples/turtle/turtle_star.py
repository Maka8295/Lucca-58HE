# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
from adafruit_turtle import Color, turtle

turtle = turtle(board.DISPLAY)
starsize = min(board.DISPLAY.width, board.DISPLAY.height) * 0.9  # 90% of screensize

print("Turtle time! Lets draw a star")

turtle.pencolor(Color.BLUE)
turtle.setheading(90)

turtle.penup()
turtle.goto(-starsize / 2, 0)
turtle.pendown()

start = turtle.pos()
while True:
    turtle.forward(starsize)
    turtle.left(170)
    if abs(turtle.pos() - start) < 1:
        break

while True:
    pass
