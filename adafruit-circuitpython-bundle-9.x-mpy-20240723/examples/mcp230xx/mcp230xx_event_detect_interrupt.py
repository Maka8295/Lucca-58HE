# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
#
# SPDX-License-Identifier: MIT

from time import sleep

import board
import busio
from digitalio import Direction, Pull
from RPi import GPIO
from adafruit_mcp230xx.mcp23017 import MCP23017

# Initialize the I2C bus:
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize the MCP23017 chip on the bonnet
mcp = MCP23017(i2c)

# Optionally change the address of the device if you set any of the A0, A1, A2
# pins.  Specify the new address with a keyword parameter:
# mcp = MCP23017(i2c, address=0x21)  # MCP23017 w/ A0 set

# Make a list of all the pins (a.k.a 0-16)
pins = []
for pin in range(0, 16):
    pins.append(mcp.get_pin(pin))

# Set all the pins to input
for pin in pins:
    pin.direction = Direction.INPUT
    pin.pull = Pull.UP

# Set up to check all the port B pins (pins 8-15) w/interrupts!
mcp.interrupt_enable = 0xFFFF  # Enable Interrupts in all pins
# If intcon is set to 0's we will get interrupts on
# both button presses and button releases
mcp.interrupt_configuration = 0x0000  # interrupt on any change
mcp.io_control = 0x44  # Interrupt as open drain and mirrored
mcp.clear_ints()  # Interrupts need to be cleared initially

# Or, we can ask to be notified CONTINUOUSLY if a pin goes LOW (button press)
# we won't get an IRQ pulse when the pin is HIGH!
# mcp.interrupt_configuration = 0xFFFF         # notify pin value
# mcp.default_value = 0xFFFF         # default value is 'high' so notify whenever 'low'


def print_interrupt(port):
    """Callback function to be called when an Interrupt occurs."""
    for pin_flag in mcp.int_flag:
        print("Interrupt connected to Pin: {}".format(port))
        print("Pin number: {} changed to: {}".format(pin_flag, pins[pin_flag].value))
    mcp.clear_ints()


# connect either interrupt pin to the Raspberry pi's pin 17.
# They were previously configured as mirrored.
GPIO.setmode(GPIO.BCM)
interrupt = 17
GPIO.setup(interrupt, GPIO.IN, GPIO.PUD_UP)  # Set up Pi's pin as input, pull up

# The add_event_detect fuction will call our print_interrupt callback function
# every time an interrupt gets triggered.
GPIO.add_event_detect(interrupt, GPIO.FALLING, callback=print_interrupt, bouncetime=10)

# The following lines are so the program runs for at least 60 seconds,
# during that time it will detect any pin interrupt and print out the pin number
# that changed state and its current state.
# The program can be terminated using Ctrl+C. It doesn't matter how it
# terminates it will always run GPIO.cleanup().
try:
    print("When button is pressed you'll see a message")
    sleep(60)  # You could run your main while loop here.
    print("Time's up. Finished!")
finally:
    GPIO.cleanup()
