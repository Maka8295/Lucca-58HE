# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Quick test of RA8875 with Feather M4
import time
import busio
import digitalio
import board

from adafruit_ra8875 import ra8875
from adafruit_ra8875.ra8875 import color565

BLACK = color565(0, 0, 0)
RED = color565(255, 0, 0)
BLUE = color565(0, 255, 0)
GREEN = color565(0, 0, 255)
YELLOW = color565(255, 255, 0)
CYAN = color565(0, 255, 255)
MAGENTA = color565(255, 0, 255)
WHITE = color565(255, 255, 255)

# Configuration for CS and RST pins:
cs_pin = digitalio.DigitalInOut(board.D9)
rst_pin = digitalio.DigitalInOut(board.D10)
int_pin = digitalio.DigitalInOut(board.D11)

# Config for display baudrate (default max is 6mhz):
BAUDRATE = 6000000

# Setup SPI bus using hardware SPI:
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Create and setup the RA8875 display:
display = ra8875.RA8875(spi, cs=cs_pin, rst=rst_pin, baudrate=BAUDRATE)
display.init()

display.fill(RED)
time.sleep(0.500)
display.fill(YELLOW)
time.sleep(0.500)
display.fill(BLUE)
time.sleep(0.500)
display.fill(CYAN)
time.sleep(0.500)
display.fill(MAGENTA)
time.sleep(0.500)
display.fill(BLACK)
display.circle(100, 100, 50, BLACK)
display.fill_circle(100, 100, 49, BLUE)

display.fill_rect(10, 10, 400, 200, GREEN)
display.rect(10, 10, 400, 200, BLUE)
display.fill_round_rect(200, 10, 200, 100, 10, RED)
display.round_rect(200, 10, 200, 100, 10, BLUE)
display.pixel(10, 10, BLACK)
display.pixel(11, 11, BLACK)
display.line(10, 10, 200, 100, RED)
display.fill_triangle(200, 15, 250, 100, 150, 125, YELLOW)
display.triangle(200, 15, 250, 100, 150, 125, BLACK)
display.fill_ellipse(300, 100, 100, 40, BLUE)
display.ellipse(300, 100, 100, 40, RED)
display.curve(50, 100, 80, 40, 2, BLACK)
display.fill_curve(50, 100, 78, 38, 2, WHITE)

display.txt_set_cursor(display.width // 2 - 200, display.height // 2 - 20)
display.txt_trans(WHITE)
display.txt_size(2)
testvar = 99
display.txt_write("Player Score: " + str(testvar))

display.touch_init(int_pin)
display.touch_enable(True)

x_scale = 1024 / display.width
y_scale = 1024 / display.height

# Main loop:
while True:
    if display.touched():
        coords = display.touch_read()
        display.fill_circle(
            int(coords[0] / x_scale), int(coords[1] / y_scale), 4, MAGENTA
        )
        display.txt_color(WHITE, BLACK)
        display.txt_set_cursor(display.width // 2 - 220, display.height // 2 - 20)
        display.txt_size(2)
        display.txt_write(
            "Position ("
            + str(int(coords[0] / x_scale))
            + ", "
            + str(int(coords[1] / y_scale))
            + ")"
        )
