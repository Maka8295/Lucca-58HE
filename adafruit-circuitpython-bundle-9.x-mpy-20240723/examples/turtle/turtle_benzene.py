# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
from adafruit_turtle import Color, turtle

turtle = turtle(board.DISPLAY)
benzsize = min(board.DISPLAY.width, board.DISPLAY.height) * 0.5

print("Turtle time! Lets draw a rainbow benzene")

colors = (Color.RED, Color.ORANGE, Color.YELLOW, Color.GREEN, Color.BLUE, Color.PURPLE)

turtle.pendown()
start = turtle.pos()

for x in range(benzsize):
    turtle.pencolor(colors[x % 6])
    turtle.forward(x)
    turtle.left(59)

while True:
    pass
