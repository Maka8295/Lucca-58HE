# SPDX-FileCopyrightText: 2022 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# -----[Example for one led]-----------------------------

import asyncio
import board
import digitalio


async def blink(pin, interval, count):  # Don't forget the async!
    with digitalio.DigitalInOut(pin) as led:
        led.switch_to_output(value=False)
        for _ in range(count):
            led.value = True
            await asyncio.sleep(interval)  # Don't forget the await!
            led.value = False
            await asyncio.sleep(interval)  # Don't forget the await!


async def main():  # Don't forget the async!
    led_task = asyncio.create_task(blink(board.D1, 0.25, 10))
    await asyncio.gather(led_task)  # Don't forget the await!
    print("done")


asyncio.run(main())


# -----[Example for two leds]-------------------------------

# Import modules as above


async def blink(pin, interval, count):
    # pylint: disable=function-redefined
    with digitalio.DigitalInOut(pin) as led:
        led.switch_to_output(value=False)
        for _ in range(count):
            led.value = True
            await asyncio.sleep(interval)  # Don't forget the "await"!
            led.value = False
            await asyncio.sleep(interval)  # Don't forget the "await"!


async def main():
    # pylint: disable=function-redefined
    led1_task = asyncio.create_task(blink(board.D1, 0.25, 10))
    led2_task = asyncio.create_task(blink(board.D2, 0.1, 20))

    await asyncio.gather(led1_task, led2_task)  # Don't forget "await"!
    print("done")


asyncio.run(main())
