# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Use custom characters to display Nyan cat"""
import time
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2

# Metro M0/M4 Pin Config:
lcd_rs = digitalio.DigitalInOut(board.D7)
lcd_en = digitalio.DigitalInOut(board.D8)
lcd_d7 = digitalio.DigitalInOut(board.D12)
lcd_d6 = digitalio.DigitalInOut(board.D11)
lcd_d5 = digitalio.DigitalInOut(board.D10)
lcd_d4 = digitalio.DigitalInOut(board.D9)
lcd_backlight = digitalio.DigitalInOut(board.D13)

# Initialise the LCD class
lcd = characterlcd.Character_LCD_Mono(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight
)

head = [31, 17, 27, 17, 17, 21, 17, 31]

top_body = [31, 0, 31, 0, 18, 8, 2, 8]
top_left_corner_body = [31, 16, 16, 17, 22, 20, 20, 20]
top_right_corner_body = [31, 1, 1, 17, 13, 5, 5, 5]

# these three chars will be the above three reversed with a few minor changes to
# fit feet into the bottom
bot_body = []
bot_left_corner_body = []
bot_right_corner_body = []

tail_neutral = [0, 0, 0, 0, 31, 31, 0, 0]
tail_up = [0, 8, 12, 6, 3, 1, 0, 0]

for i in range(7, -1, -1):
    bot_body.append(top_body[i])
    bot_left_corner_body.append(top_left_corner_body[i])
    bot_right_corner_body.append(top_right_corner_body[i])

# adding feet and making space for them

bot_body[6] = 31
bot_body[5] = 0
bot_body[4] = 31
bot_body[7] = 24
bot_left_corner_body[7] = 0
bot_left_corner_body[6] = 31
bot_left_corner_body[7] = 28
bot_right_corner_body[7] = 0
bot_right_corner_body[6] = 31

# bottom body with feet forward
bot_body2 = bot_body[:-1] + [3]


rainbow = [0, 0, 6, 25, 11, 29, 27, 12]
rainbow2 = [0, 0, 6, 31, 13, 5, 23, 12]

lcd.create_char(0, top_body)
lcd.create_char(1, top_left_corner_body)
lcd.create_char(2, rainbow)
lcd.create_char(3, bot_left_corner_body)
lcd.create_char(4, bot_body)
lcd.create_char(5, bot_right_corner_body)
lcd.create_char(6, head)
lcd.create_char(7, tail_neutral)

lcd.clear()

lcd.move_right()
lcd.message = (
    "\x02\x02\x02\x02\x01\x00\x00\x00\x06\n\x02\x02\x02\x07\x03\x04\x04\x04\x05"
)

lcd.backlight = True

while True:
    lcd.create_char(4, bot_body2)
    lcd.create_char(7, tail_up)
    lcd.create_char(2, rainbow2)
    lcd.move_right()
    time.sleep(0.4)
    lcd.create_char(4, bot_body)
    lcd.create_char(7, tail_neutral)
    lcd.create_char(2, rainbow)
    lcd.move_left()
    time.sleep(0.4)
