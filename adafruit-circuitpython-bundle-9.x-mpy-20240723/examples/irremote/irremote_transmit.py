# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""IR transmit example using Circuit Playground Express"""
# pylint: disable-msg=no-member
import time
import pulseio
import board
import digitalio
import adafruit_irremote

# Create a button object to trigger IR transmit
button = digitalio.DigitalInOut(board.D4)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.DOWN

# Create a 'PulseOut' to send infrared signals on the IR transmitter @ 38KHz
pulseout = pulseio.PulseOut(board.IR_TX, frequency=38000, duty_cycle=2**15)
# Create an encoder that will take numbers and turn them into NEC IR pulses
encoder = adafruit_irremote.GenericTransmit(
    header=[9000, 4500], one=[560, 1700], zero=[560, 560], trail=560
)

while True:
    if button.value:
        print("IR signal sent!")
        encoder.transmit(pulseout, [255, 2, 255, 0])
        time.sleep(0.2)
