# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""THIS EXAMPLE REQUIRES A SEPARATE LIBRARY BE LOADED ONTO YOUR CIRCUITPY DRIVE.
This example requires the adafruit_irremote.mpy library.

THIS EXAMPLE WORKS WITH CIRCUIT PLAYGROUND EXPRESS ONLY.

This example uses the IR receiver found near the center of the board. Works with another Circuit
Playground Express running the circuitplayground_ir_transmit.py example. The NeoPixels will light
up when the buttons on the TRANSMITTING Circuit Playground Express are pressed!"""
import pulseio
import board
import adafruit_irremote
from adafruit_circuitplayground import cp

# Create a 'pulseio' input, to listen to infrared signals on the IR receiver
try:
    pulsein = pulseio.PulseIn(board.IR_RX, maxlen=120, idle_state=True)
except AttributeError as err:
    raise NotImplementedError(
        "This example does not work with Circuit Playground Bluefruti!"
    ) from err

# Create a decoder that will take pulses and turn them into numbers
decoder = adafruit_irremote.GenericDecode()

while True:
    cp.red_led = True
    pulses = decoder.read_pulses(pulsein)
    try:
        # Attempt to convert received pulses into numbers
        received_code = decoder.decode_bits(pulses)
    except adafruit_irremote.IRNECRepeatException:
        # We got an unusual short code, probably a 'repeat' signal
        continue
    except adafruit_irremote.IRDecodeException:
        # Something got distorted
        continue

    print("Infrared code received: ", received_code)
    if received_code == [66, 84, 78, 65]:
        print("Button A signal")
        cp.pixels.fill((100, 0, 155))
    if received_code == [66, 84, 78, 64]:
        print("Button B Signal")
        cp.pixels.fill((210, 45, 0))
