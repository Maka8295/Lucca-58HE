# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple test for RGB character LCD on Raspberry Pi"""
import time
import board
import digitalio
import pwmio
import adafruit_character_lcd.character_lcd as characterlcd

# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2

# Raspberry Pi Pin Config:
lcd_rs = digitalio.DigitalInOut(board.D26)  # LCD pin 4
lcd_en = digitalio.DigitalInOut(board.D19)  # LCD pin 6
lcd_d7 = digitalio.DigitalInOut(board.D27)  # LCD pin 14
lcd_d6 = digitalio.DigitalInOut(board.D22)  # LCD pin 13
lcd_d5 = digitalio.DigitalInOut(board.D24)  # LCD pin 12
lcd_d4 = digitalio.DigitalInOut(board.D25)  # LCD pin 11
lcd_rw = digitalio.DigitalInOut(
    board.D4
)  # LCD pin 5.  Determines whether to read to or write from the display.
# Not necessary if only writing to the display. Used on shield.

red = pwmio.PWMOut(board.D21)
green = pwmio.PWMOut(board.D12)
blue = pwmio.PWMOut(board.D18)

# Initialize the LCD class
# The lcd_rw parameter is optional.  You can omit the line below if you're only
# writing to the display.
lcd = characterlcd.Character_LCD_RGB(
    lcd_rs,
    lcd_en,
    lcd_d4,
    lcd_d5,
    lcd_d6,
    lcd_d7,
    lcd_columns,
    lcd_rows,
    red,
    green,
    blue,
    lcd_rw,
)

RED = [100, 0, 0]
GREEN = [0, 100, 0]
BLUE = [0, 0, 100]

while True:
    lcd.clear()
    # Set LCD color to red
    lcd.color = [100, 0, 0]
    time.sleep(1)

    # Print two line message
    lcd.message = "Hello\nCircuitPython"

    # Wait 5s
    time.sleep(5)

    # Set LCD color to blue
    lcd.color = [0, 100, 0]
    time.sleep(1)
    # Set LCD color to green
    lcd.color = [0, 0, 100]
    time.sleep(1)
    # Set LCD color to purple
    lcd.color = [50, 0, 50]
    time.sleep(1)
    lcd.clear()

    # Print two line message right to left
    lcd.text_direction = lcd.RIGHT_TO_LEFT
    lcd.message = "Hello\nCircuitPython"
    # Wait 5s
    time.sleep(5)

    # Return text direction to left to right
    lcd.text_direction = lcd.LEFT_TO_RIGHT

    # Display cursor
    lcd.clear()
    lcd.cursor = True
    lcd.message = "Cursor! "
    # Wait 5s
    time.sleep(5)

    # Display blinking cursor
    lcd.clear()
    lcd.blink = True
    lcd.message = "Blinky Cursor!"
    # Wait 5s
    time.sleep(5)
    lcd.blink = False
    lcd.clear()

    # Create message to scroll
    scroll_msg = "<-- Scroll"
    lcd.message = scroll_msg
    # Scroll to the left
    for i in range(len(scroll_msg)):
        time.sleep(0.5)
        lcd.move_left()
    lcd.clear()

    # Turn off LCD backlights and clear text
    lcd.color = [0, 0, 0]
    lcd.clear()
    time.sleep(1)
