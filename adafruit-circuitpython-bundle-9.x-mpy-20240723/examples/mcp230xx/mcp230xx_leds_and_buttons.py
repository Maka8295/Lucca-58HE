# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import board
import busio
from digitalio import Direction, Pull
from adafruit_mcp230xx.mcp23017 import MCP23017

# Initialize the I2C bus:
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize the MCP23017 chip on the bonnet
mcp = MCP23017(i2c)

# Optionally change the address of the device if you set any of the A0, A1, A2
# pins.  Specify the new address with a keyword parameter:
# mcp = MCP23017(i2c, address=0x21)  # MCP23017 w/ A0 set

# Make a list of all the port A pins (a.k.a 0-7)
port_a_pins = []
for pin in range(0, 8):
    port_a_pins.append(mcp.get_pin(pin))

# Make a list of all the port B pins (a.k.a 8-15)
port_b_pins = []
for pin in range(8, 16):
    port_b_pins.append(mcp.get_pin(pin))

# Set all the port A pins to output
for pin in port_a_pins:
    pin.direction = Direction.OUTPUT

# Set all the port B pins to input, with pullups!
for pin in port_b_pins:
    pin.direction = Direction.INPUT
    pin.pull = Pull.UP

# Turn on all port A pins for 1/10 of a second
# while True:
#    for pin in port_a_pins:
#        pin.value = True    # turn LED on!
#        time.sleep(0.1)     # wait 0.1 seconds
#        pin.value = False   # turn LED off

while True:
    for num, button in enumerate(port_b_pins):
        if not button.value:
            print("Button #", num, "pressed!")
            # turn on matching port A pin
            port_a_pins[num].value = True  # turn LED on!
        else:
            port_a_pins[num].value = False  # turn LED off
