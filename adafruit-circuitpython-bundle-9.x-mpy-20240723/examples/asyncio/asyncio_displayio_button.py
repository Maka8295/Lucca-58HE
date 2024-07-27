# SPDX-FileCopyrightText: 2022 Tim Cocks for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
Example that illustrates how to use Displayio Buttons to modify
some blinking circles. One button inverts colors, the others change
the interval length of the blink for one of the circles.
"""

import asyncio
import adafruit_touchscreen
import displayio
import terminalio
import vectorio
import board
from adafruit_button import Button

# use built-in display
display = board.DISPLAY

# explicitly set the display to default orientation in-case it was changed
display.rotation = 0

# --| Button Config |-------------------------------------------------
# invert color Button
BUTTON_1_X = 10
BUTTON_1_Y = 80
BUTTON_1_LABEL = "Invert Color"

# slower interval Button
BUTTON_2_X = 200
BUTTON_2_Y = 160
BUTTON_2_LABEL = "Slower"

# faster interval Button
BUTTON_3_X = 200
BUTTON_3_Y = 80
BUTTON_3_LABEL = "Faster"

# shared button configurations
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
BUTTON_STYLE = Button.ROUNDRECT
BUTTON_FILL_COLOR = 0x00FFFF
BUTTON_OUTLINE_COLOR = 0xFF00FF
BUTTON_LABEL_COLOR = 0x000000
# --| Button Config |-------------------------------------------------

# Setup touchscreen (PyPortal)
ts = adafruit_touchscreen.Touchscreen(
    board.TOUCH_XL,
    board.TOUCH_XR,
    board.TOUCH_YD,
    board.TOUCH_YU,
    calibration=((5200, 59000), (5800, 57000)),
    size=(display.width, display.height),
)

# initialize color button
invert_color_btn = Button(
    x=BUTTON_1_X,
    y=BUTTON_1_Y,
    width=BUTTON_WIDTH,
    height=BUTTON_HEIGHT,
    style=BUTTON_STYLE,
    fill_color=BUTTON_FILL_COLOR,
    outline_color=BUTTON_OUTLINE_COLOR,
    label=BUTTON_1_LABEL,
    label_font=terminalio.FONT,
    label_color=BUTTON_LABEL_COLOR,
)

# initialize interval slower button
interval_slower_btn = Button(
    x=BUTTON_2_X,
    y=BUTTON_2_Y,
    width=BUTTON_WIDTH,
    height=BUTTON_HEIGHT,
    style=BUTTON_STYLE,
    fill_color=BUTTON_FILL_COLOR,
    outline_color=BUTTON_OUTLINE_COLOR,
    label=BUTTON_2_LABEL,
    label_font=terminalio.FONT,
    label_color=BUTTON_LABEL_COLOR,
)

# initialize interval faster button
interval_faster_btn = Button(
    x=BUTTON_3_X,
    y=BUTTON_3_Y,
    width=BUTTON_WIDTH,
    height=BUTTON_HEIGHT,
    style=BUTTON_STYLE,
    fill_color=BUTTON_FILL_COLOR,
    outline_color=BUTTON_OUTLINE_COLOR,
    label=BUTTON_3_LABEL,
    label_font=terminalio.FONT,
    label_color=BUTTON_LABEL_COLOR,
)


# Button state data object. Will hold either true of false whether button is currently pressed
class ButtonState:
    # pylint: disable=too-few-public-methods
    def __init__(self, initial_state):
        self.state = initial_state


# Interval length data object. Holds the amount of time in ms the interval should last for
class Interval:
    # pylint: disable=too-few-public-methods
    def __init__(self, initial_value):
        self.value = initial_value


# main group to show things on the display
main_group = displayio.Group()

# Initialize first circle
palette_1 = displayio.Palette(2)
palette_1[0] = 0x125690
palette_1[1] = 0x125690
circle_1 = vectorio.Circle(pixel_shader=palette_1, radius=15, x=20, y=20)

# Initialize second circle
palette_2 = displayio.Palette(2)
palette_2[0] = 0x12FF30
palette_2[1] = 0x12FF30
circle_2 = vectorio.Circle(pixel_shader=palette_2, radius=15, x=60, y=20)

# add everything to the group, so it gets displayed
main_group.append(circle_1)
main_group.append(circle_2)
main_group.append(invert_color_btn)
main_group.append(interval_slower_btn)
main_group.append(interval_faster_btn)


async def blink(palette, interval, count, button_state):  # Don't forget the async!
    """
    blink coroutine. Hides and shows a vectorio shape by
    using make_transparent() and make_opaque() on it's palette.

    :param displayio.Palette palette: The palette to change colors on for blinking
    :param Interval interval: The Interval data object containing the interval length to use
    :param int count: The number of times to repeat the blink. -1 for indefinite loop
    :param ButtonState button_state: The ButtonState data object for the invert color button
    """
    while count < 0 or count > 0:
        # if the color button is pressed
        if button_state.state:
            # if the color is still on default
            if palette[0] == palette[1]:
                # invert the color by subtracting from white
                palette[0] = 0xFFFFFF - palette[0]

        # if the color button is not pressed
        else:
            # set the color back to default
            palette[0] = palette[1]

        # hide the circle
        palette.make_opaque(0)
        # wait interval length
        await asyncio.sleep(interval.value / 1000)  # Don't forget the await!

        # show the circle
        palette.make_transparent(0)
        # wait interval length
        await asyncio.sleep(interval.value / 1000)  # Don't forget the await!

        # decrement count if it's positive
        if count > 0:
            count -= 1


def handle_color_button(touch_event, color_button, button_state):
    """
    Check if the color button is pressed, and updates
    the ButtonState data object as appropriate

    :param touch_event: The touch point object from touchscreen
    :param Button color_button: The button to check for presses on
    :param ButtonState button_state: ButtonState data object to set
     the current value into
    """

    # if there is a touch event
    if touch_event:
        # if the color button is being touched
        if color_button.contains(touch_event):
            # set selected to change button color
            color_button.selected = True
            # set button_state so other coroutines can access it
            button_state.state = True

        # the color button is not being touched
        else:
            # set selected to change button color back to default
            color_button.selected = False  # if touch is dragged outside of button
            # set button_state so other coroutines can access it.
            button_state.state = False

    # there are no touch events
    else:
        # if the color button is currently the pressed color
        if color_button.selected:
            # set selected back to false to change button back to default color
            color_button.selected = False
            # set button_state so other coroutines can access it
            button_state.state = False


def handle_interval_buttons(touch_event, button_slower, button_faster, interval):
    """
    Will check for presses on
    the faster and slower buttons and updated the data in the
    Interval data object as appropriate

    :param touch_event: Touch point object from touchscreen
    :param Button button_slower: The slower button object
    :param Button button_faster: The faster button object
    :param Interval interval: The Interval data object to store state
    """
    # if there are any touch events
    if touch_event:
        # if the slower button is being touched
        if button_slower.contains(touch_event):
            # if it just became pressed. i.e. was not pressed last frame
            if not button_slower.selected:
                # set selected to change the button color
                button_slower.selected = True

                # increment the interval length and store it on the data object
                interval.value += 100
                print("new interval val: {}".format(interval.value))

        # if the slower button is not being touched
        else:
            # set selected to put the slower button back to default color
            button_slower.selected = False

        # if the faster button is being touched
        if button_faster.contains(touch_event):
            # if it just became pressed. i.e. was not pressed last frame
            if not button_faster.selected:
                # set selected to change the button color
                button_faster.selected = True
                # if the interval is large enough to decrement
                if interval.value >= 100:
                    # decrement interval value and store it on the data object
                    interval.value -= 100
                print("new interval val: {}".format(interval.value))

        # if the faster button is not being touched
        else:
            # set selected back to false to change color back to default
            button_faster.selected = False

    # there are no touch events
    else:
        # if slower button is the pressed color
        if button_slower.selected:
            # set it back to default color
            button_slower.selected = False

        # if the faster button is pressed color
        if button_faster.selected:
            # set it back to default color
            button_faster.selected = False


async def monitor_buttons(
    button_slower, button_faster, color_button, interval, button_state
):
    """
    monitor_buttons coroutine.

    :param Button button_slower: The slower button object
    :param Button button_faster: The faster button object
    :param Button color_button: The invert color button object
    :param Interval interval: The Interval data object to store state
    :param ButtonState button_state: The ButtonState data object to
     store color button state
    """
    while True:
        # get current touch data from overlay
        p = ts.touch_point

        # handle touch event data
        handle_color_button(p, color_button, button_state)
        handle_interval_buttons(p, button_slower, button_faster, interval)

        # allow other tasks to do work
        await asyncio.sleep(0)


# main coroutine
async def main():  # Don't forget the async!
    # create data objects
    color_btn_state = ButtonState(False)
    interval_1 = Interval(550)
    interval_2 = Interval(350)

    # create circle blink tasks
    circle_1_task = asyncio.create_task(
        blink(palette_1, interval_1, -1, color_btn_state)
    )
    circle_2_task = asyncio.create_task(
        blink(palette_2, interval_2, 20, color_btn_state)
    )

    # create buttons task
    button_task = asyncio.create_task(
        monitor_buttons(
            interval_slower_btn,
            interval_faster_btn,
            invert_color_btn,
            interval_1,
            color_btn_state,
        )
    )

    # start all of the tasks
    await asyncio.gather(
        circle_1_task, circle_2_task, button_task
    )  # Don't forget the await!


# show main_group so it's visible on the display
display.root_group = main_group

# start the main coroutine
asyncio.run(main())
