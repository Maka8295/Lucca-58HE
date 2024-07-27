# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# pylint: disable=unnecessary-lambda-assignment

import board
from adafruit_turtle import turtle


def hilbert2(step, rule, angle, depth, t):
    if depth > 0:
        a = lambda: hilbert2(step, "a", angle, depth - 1, t)
        b = lambda: hilbert2(step, "b", angle, depth - 1, t)
        left = lambda: t.left(angle)
        right = lambda: t.right(angle)
        forward = lambda: t.forward(step)
        if rule == "a":
            left()
            b()
            forward()
            right()
            a()
            forward()
            a()
            right()
            forward()
            b()
            left()
        if rule == "b":
            right()
            a()
            forward()
            left()
            b()
            forward()
            b()
            left()
            forward()
            a()
            right()


turtle = turtle(board.DISPLAY)
turtle.penup()
turtle.setheading(90)
turtle.goto(-80, -80)
turtle.pendown()
hilbert2(5, "a", 90, 5, turtle)

while True:
    pass
