# SPDX-FileCopyrightText: 2024 J Fletcher
#
# SPDX-License-Identifier: MIT

# SIMPLE ASYNCIO EVENT EXAMPLE

# Brief program that illustrates using Events to coordinate tasks
# within Asyncio programs. The present example involves only one led
# and one event, but Asyncio allows a high degree of scaling. Adding
# several copies of the functions 'blink', 'input_poll', or 'state'
# should be straightforward with changes to names and objects.

import asyncio
import board
import digitalio
from adafruit_debouncer import Debouncer
import neopixel


# Import library modules, as is tradition

pin = digitalio.DigitalInOut(board.BUTTON)
pin.direction = digitalio.Direction.INPUT
pin.pull = digitalio.Pull.UP
button = Debouncer(pin)

# Instantiate the input, in this case, the 'BOOT' button on a
# QT Py 2040. The debouncer ensures a clean hit.

BLANK = (0, 0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

COLORS = {0: BLANK, 1: RED, 2: GREEN, 3: BLUE}

# Define the various colors according to preference and set them into
# a dictionary for later retrieval. (Blue is not used in this code.)


class Color:
    # pylint: disable=too-few-public-methods
    def __init__(self, initial_value):
        self.value = initial_value


# Create a class to hold and track the color while code executes.


async def blink(color):
    with neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.1) as led:
        while True:
            led[0] = COLORS.get(0)
            await asyncio.sleep(1)
            led[0] = COLORS.get(color.value)
            await asyncio.sleep(0)


# Instantiate the led using 'with ... as' construction to keep this
# function from blocking. 'COLORS.get(0)' indicates the led should show
# no color (i.e., turn off), while 'COLORS.get(color.value)' instructs
# the led to show the color pulled from the dictionary via the color
# class' color.value. The line 'asyncio.sleep(1)' sets the blink rate;
# in this case, once per second.


async def input_poll(swapper):
    count = 0
    while True:
        button.update()
        if button.fell:
            print("Press!")
            if count == 0:
                count += 1
                print("Event is set!")
                swapper.set()
            elif count == 1:
                count -= 1
                print("Event is clear!")
                swapper.clear()
        await asyncio.sleep(0)


# This function checks the button for activity and sets or clears the
# Event depending on the button activity reflected in the 'count' variable.
# The count begins set at 0 and is alternatingly incremented (count += 1)
# and decremented (count -= 1) with each press of the button.


async def state(swapper, color):
    while True:
        if swapper.is_set():
            color.value = 2
        else:
            color.value = 1
        await asyncio.sleep(0)


async def main():
    color = Color(1)
    COLORS.get(color)

    # Sets the color the led will first show on start

    swapper = asyncio.Event()

    # Creates and names the Event that signals the led to change color

    blinky = asyncio.create_task(blink(color))
    poll = asyncio.create_task(input_poll(swapper))
    monitor = asyncio.create_task(state(swapper, color))

    # Creates and names Tasks from the functions defined above

    await asyncio.gather(monitor, blinky, poll)


# Don't forget the 'await'! The 'asyncio.gather()' command passes the
# listed tasks to the asynchronous scheduler, where processing resources
# are directed from one task to another depending upon whether said task
# has signalled its ability to 'give up' control by reaching the 'await
# asyncio.sleep()' line.

asyncio.run(main())
