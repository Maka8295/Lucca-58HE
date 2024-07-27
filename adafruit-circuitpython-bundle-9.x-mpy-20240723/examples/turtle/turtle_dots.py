# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
from adafruit_turtle import turtle

print("Turtle time! Lets draw a square with dots")

turtle = turtle(board.DISPLAY)
turtle.pendown()

for _ in range(4):
    turtle.dot(8)
    turtle.left(90)
    turtle.forward(25)

while True:
    pass
