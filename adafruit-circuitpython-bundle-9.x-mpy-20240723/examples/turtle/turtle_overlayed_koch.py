# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# pylint: disable=unnecessary-lambda-assignment

import board
from adafruit_turtle import turtle, Color

generation_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW]


def f(side_length, depth, generation):
    if depth == 0:
        turtle.forward(side_length)
        return
    side = lambda: f(side_length / 3, depth - 1, generation + 1)
    side()
    turtle.left(60)
    side()
    turtle.right(120)
    side()
    turtle.left(60)
    side()


def snowflake(num_generations, generation_color):
    top_side = lambda: f(top_len, num_generations, 0)
    turtle.pencolor(generation_color)
    top_side()
    turtle.right(120)
    top_side()
    turtle.right(120)
    top_side()


turtle = turtle(board.DISPLAY)

unit = min(board.DISPLAY.width / 3, board.DISPLAY.height / 4)
top_len = unit * 3
print(top_len)
turtle.setheading(90)

turtle.penup()
turtle.goto(-1.5 * unit, unit)
turtle.pendown()

for generations in range(4):
    snowflake(generations, generation_colors[generations])
    turtle.right(120)

while True:
    pass
