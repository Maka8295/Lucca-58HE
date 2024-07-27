# SPDX-FileCopyrightText: 2023 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Quad I2C rotary encoder NeoPixel color picker example."""
import board
from rainbowio import colorwheel
import digitalio
import adafruit_seesaw.seesaw
import adafruit_seesaw.neopixel
import adafruit_seesaw.rotaryio
import adafruit_seesaw.digitalio

# For boards/chips that don't handle clock-stretching well, try running I2C at 50KHz
# import busio
# i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
# For using the built-in STEMMA QT connector on a microcontroller
i2c = board.STEMMA_I2C()
seesaw = adafruit_seesaw.seesaw.Seesaw(i2c, 0x49)

encoders = [adafruit_seesaw.rotaryio.IncrementalEncoder(seesaw, n) for n in range(4)]
switches = [adafruit_seesaw.digitalio.DigitalIO(seesaw, pin) for pin in (12, 14, 17, 9)]
for switch in switches:
    switch.switch_to_input(digitalio.Pull.UP)  # input & pullup!

# four neopixels per PCB
pixels = adafruit_seesaw.neopixel.NeoPixel(seesaw, 18, 4)
pixels.brightness = 0.5

last_positions = [-1, -1, -1, -1]
colors = [0, 0, 0, 0]  # start at red

while True:
    # negate the position to make clockwise rotation positive
    positions = [encoder.position for encoder in encoders]
    print(positions)
    for n, rotary_pos in enumerate(positions):
        if rotary_pos != last_positions[n]:
            if switches[n].value:  # Change the LED color if switch is not pressed
                if (
                    rotary_pos > last_positions[n]
                ):  # Advance forward through the colorwheel.
                    colors[n] += 8
                else:
                    colors[n] -= 8  # Advance backward through the colorwheel.
                colors[n] = (colors[n] + 256) % 256  # wrap around to 0-256
            # Set last position to current position after evaluating
            print(f"Rotary #{n}: {rotary_pos}")
            last_positions[n] = rotary_pos

        # if switch is pressed, light up white, otherwise use the stored color
        if not switches[n].value:
            pixels[n] = 0xFFFFFF
        else:
            pixels[n] = colorwheel(colors[n])
