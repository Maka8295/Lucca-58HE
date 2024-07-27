# SPDX-FileCopyrightText: 2022 Jeff Epler for Adafruit Industries
# SPDX-License-Identifier: MIT

# pylint: disable=consider-using-with

import asyncio
from displayio import TileGrid, OnDiskBitmap, Group
from rainbowio import colorwheel
from adafruit_pybadger import pybadger

# If you choose to enter a pronoun it's shown on the "business card" page
pronoun = ""
custom_line1 = "FIRST"
custom_line2 = "LAST"  # also a great place to show a pronoun

# Set up the custom image
qr_image = OnDiskBitmap(open("/QR_Blinka_CircuitPythonOrg.bmp", "rb"))
qr_tg = TileGrid(qr_image, pixel_shader=qr_image.pixel_shader)
qr_gp = Group()
qr_gp.append(qr_tg)

pybadger.badge_background(
    background_color=pybadger.WHITE,
    rectangle_color=pybadger.PURPLE,
    rectangle_drop=0.25,
    rectangle_height=0.55,
)

pybadger.badge_line(
    text="HELLO I'M", color=pybadger.BLINKA_PURPLE, scale=2, padding_above=1
)
pybadger.badge_line(text=custom_line1, color=pybadger.WHITE, scale=6, padding_above=1)
pybadger.badge_line(
    text=custom_line2, color=pybadger.BLINKA_PURPLE, scale=2, padding_above=0.25
)

# Start with the custom badge page
pybadger.show_custom_badge()


# This task responds to buttons and changes the visible page
async def ui_task():
    while True:
        if pybadger.button.a:
            pybadger.show_business_card(
                image_name="Blinka.bmp",
                name_string="Jeff Epler",
                name_scale=2,
                email_string_one="jeff@adafruit.com",
                email_string_two=pronoun,
            )
        elif pybadger.button.b:
            pybadger.root_group = qr_gp
        elif pybadger.button.start:
            pybadger.show_custom_badge()
        elif pybadger.button.select:
            pybadger.activity()
        else:
            pybadger.auto_dim_display(
                delay=0.5
            )  # Remove or comment out this line if you have the PyBadge LC
        await asyncio.sleep(0.02)


# This task animates the LEDs
async def led_task():
    pixels = pybadger.pixels
    pixels.auto_write = False
    num_pixels = len(pixels)
    j = 0
    while True:
        bright = pybadger.display.brightness > 0.5
        j = (j + (7 if bright else 3)) & 255
        b = 31 / 255.0 if bright else 5 / 255.0
        if pixels.brightness != b:
            pixels.brightness = b
        for i in range(num_pixels):
            rc_index = i * 97 + j
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        await asyncio.sleep(0.02)


# Run both tasks via asyncio!
async def main():
    await asyncio.gather(ui_task(), led_task())


asyncio.run(main())
