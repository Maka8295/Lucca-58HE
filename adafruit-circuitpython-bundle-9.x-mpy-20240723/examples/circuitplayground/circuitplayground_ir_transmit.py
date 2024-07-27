# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""THIS EXAMPLE REQUIRES A SEPARATE LIBRARY BE LOADED ONTO YOUR CIRCUITPY DRIVE.
This example requires the adafruit_irremote.mpy library.

THIS EXAMPLE WORKS WITH CIRCUIT PLAYGROUND EXPRESS ONLY.

This example uses the IR transmitter found near the center of the board. Works with another Circuit
Playground Express running the circuitplayground_ir_receive.py example. Press the buttons to light
up the NeoPixels on the RECEIVING Circuit Playground Express!"""
import time
import pulseio
import board
import adafruit_irremote
from adafruit_circuitplayground import cp

# Create a 'PulseOut' output, to send infrared signals from the IR transmitter
try:
    pulseout = pulseio.PulseOut(board.IR_TX, frequency=38000, duty_cycle=2**15)
except AttributeError as err:
    # Catch no board.IR_TX pin
    raise NotImplementedError(
        "This example does not work with Circuit Playground Bluefruit!"
    ) from err

# Create an encoder that will take numbers and turn them into NEC IR pulses
encoder = adafruit_irremote.GenericTransmit(
    header=[9500, 4500], one=[550, 550], zero=[550, 1700], trail=0
)

while True:
    if cp.button_a:
        print("Button A pressed! \n")
        cp.red_led = True
        encoder.transmit(pulseout, [66, 84, 78, 65])
        cp.red_led = False
        # wait so the receiver can get the full message
        time.sleep(0.2)
    if cp.button_b:
        print("Button B pressed! \n")
        cp.red_led = True
        encoder.transmit(pulseout, [66, 84, 78, 64])
        cp.red_led = False
        time.sleep(0.2)
