# SPDX-FileCopyrightText: Copyright (c) 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
# pylint: disable=no-member
"""Display the microcontroller CPU temperature in C and F on a display."""
import microcontroller
from adafruit_simple_text_display import SimpleTextDisplay

temperature_data = SimpleTextDisplay(title="Temperature Data!", title_scale=2)

while True:
    temperature_data[0].text = "Temperature: {:.2f} degrees C".format(
        microcontroller.cpu.temperature
    )
    temperature_data[1].text = "Temperature: {:.2f} degrees F".format(
        (microcontroller.cpu.temperature * (9 / 5) + 32)
    )
    temperature_data.show()
