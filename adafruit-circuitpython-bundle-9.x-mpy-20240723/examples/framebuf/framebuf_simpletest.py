# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import math
import adafruit_framebuf

print("framebuf test will draw to the REPL")

WIDTH = 32
HEIGHT = 8

buffer = bytearray(round(WIDTH * math.ceil(HEIGHT / 8)))
fb = adafruit_framebuf.FrameBuffer(
    buffer, WIDTH, HEIGHT, buf_format=adafruit_framebuf.MVLSB
)


# Ascii printer for very small framebufs!
def print_buffer(the_fb):
    print("." * (the_fb.width + 2))
    for y in range(the_fb.height):
        print(".", end="")
        for x in range(the_fb.width):
            if fb.pixel(x, y):
                print("*", end="")
            else:
                print(" ", end="")
        print(".")
    print("." * (the_fb.width + 2))


# Small function to clear the buffer
def clear_buffer():
    for i, _ in enumerate(buffer):
        buffer[i] = 0


print("Shapes test: ")
fb.pixel(3, 5, True)
fb.rect(0, 0, fb.width, fb.height, True)
fb.line(1, 1, fb.width - 2, fb.height - 2, True)
fb.fill_rect(25, 2, 2, 2, True)
print_buffer(fb)

print("Text test: ")
# empty
fb.fill_rect(0, 0, WIDTH, HEIGHT, False)

# write some text
fb.text("hello", 0, 0, True)
print_buffer(fb)
clear_buffer()

# write some larger text
fb.text("hello", 8, 0, True, size=2)
print_buffer(fb)
