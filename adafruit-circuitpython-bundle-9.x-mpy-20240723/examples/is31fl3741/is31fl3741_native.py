# SPDX-FileCopyrightText: 2021 Mark Komus
# SPDX-License-Identifier: MIT
# Currently example only compatible with Adafruit LED Glasses Driver nRF52840
import is31fl3741
import displayio
import framebufferio
import board
import busio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.chase import Chase
from adafruit_is31fl3741.is31fl3741_PixelBuf import IS31FL3741_PixelBuf
from adafruit_is31fl3741.led_glasses_map import (
    glassesmatrix_ledmap_no_ring,
    left_ring_map_no_inner,
    right_ring_map_no_inner,
)

# Release any existing displays
displayio.release_displays()

# Create our own I2C bus with a 1Mhz frequency for faster updates
i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000)

# Initalize the IS31FL3741
is31 = is31fl3741.IS31FL3741(i2c=i2c)

# Initialize the IS31FL3741 displayio display
is31_fb = is31fl3741.IS31FL3741_FrameBuffer(
    width=54,
    height=15,
    is31=is31,
    scale=True,
    gamma=True,
    mapping=glassesmatrix_ledmap_no_ring,
)
display = framebufferio.FramebufferDisplay(is31_fb, auto_refresh=True)

# Turn the brightness down
is31_fb.brightness = 0.1

# Create pixel buffers for each eye. Init is False as the display setup initialized the chip
eye_left = IS31FL3741_PixelBuf(
    is31, left_ring_map_no_inner, init=False, auto_write=False
)
eye_right = IS31FL3741_PixelBuf(
    is31, right_ring_map_no_inner, init=False, auto_write=False
)

# Create a different animation for each eye ring
chase = Chase(eye_left, speed=0.05, color=(0, 0, 150), size=8, spacing=4)
comet = Comet(eye_right, speed=0.01, color=(0, 0, 150), tail_length=10, bounce=False)

# Create text to scroll across the display
font = bitmap_font.load_font("scrolly.bdf")
text = "HELLO FROM CIRCUITPYTHON ON NATIVE DISPLAYIO"
color = (255, 210, 0)
text_area = label.Label(font, text=text, color=color)

# Set the text location
text_width = text_area.bounding_box[2]
text_area.x = display.width
text_area.y = 8

# Add the text label to the display
group = displayio.Group()
group.append(text_area)
display.root_group = group

# Scroll the text and update the animations
x = display.width
while True:
    x = x - 1
    text_area.x = x
    if x == -text_width:
        x = display.width

    chase.animate()
    comet.animate()
