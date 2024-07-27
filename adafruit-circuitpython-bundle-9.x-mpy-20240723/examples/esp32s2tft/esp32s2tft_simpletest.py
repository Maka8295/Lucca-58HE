# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import random
from rainbowio import colorwheel
from adafruit_esp32s2tft import ESP32S2TFT

esp32s2tft = ESP32S2TFT(default_bg=0xFFFF00, scale=2, use_network=False)

# Create the labels
esp32s2tft.add_text(
    text="ESP32-S2", text_position=(10, 10), text_scale=2, text_color=0xFF00FF
)
esp32s2tft.add_text(
    text="TFT Feather",
    text_position=(60, 30),
    text_anchor_point=(0.5, 0.5),
    text_color=0xFF00FF,
)
button_label = esp32s2tft.add_text(
    text="Press BOOT0 Button",
    line_spacing=1.0,
    text_position=(60, 50),
    text_anchor_point=(0.5, 0.5),
    text_color=0x606060,
)
esp32s2tft.display.root_group = esp32s2tft.splash

while True:
    esp32s2tft.set_text_color(
        0xFF0000 if esp32s2tft.peripherals.button else 0x606060, button_label
    )
    esp32s2tft.peripherals.led = esp32s2tft.peripherals.button
    if esp32s2tft.peripherals.button:
        esp32s2tft.peripherals.neopixel[0] = colorwheel(random.randint(0, 255))
