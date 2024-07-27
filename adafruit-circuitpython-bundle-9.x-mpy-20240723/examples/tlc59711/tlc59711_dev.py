#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CircuitPython

# SPDX-FileCopyrightText: 2021 s-light
# SPDX-License-Identifier: MIT
# Author Stefan Krüger (s-light)

"""TLC5971 / TLC59711 Multi Development."""

__doc__ = """
TLC59711 development helper.

this sketch contains a bunch of timing tests and other development things..
Enjoy the colors :-)
"""

import time

import board
import busio

import adafruit_tlc59711


##########################################
PIXEL_COUNT = 16 * 1

spi = busio.SPI(board.SCK, MOSI=board.MOSI)
pixels = adafruit_tlc59711.TLC59711(spi, pixel_count=PIXEL_COUNT)


##########################################
# test function

VALUE_HIGH = 1000


def channelcheck_update_pixel(offset):
    """Channel check pixel."""
    # print("offset", offset)

    # pixels[offset] = (VALUE_HIGH, 0, 0)
    pixels.set_pixel_16bit_value(offset, VALUE_HIGH, 0, 0)
    # clear last pixel
    last = offset - 1
    if last < 0:
        last = PIXEL_COUNT - 1
    # pixels[last] = (0, 0, 1)
    pixels.set_pixel_16bit_value(last, 0, 0, 1)
    # pixels[offset] = (0xAAAA, 0xBBBB, 0xCCCC)
    pixels.show()

    offset += 1
    if offset >= PIXEL_COUNT:
        time.sleep(0.2)
        offset = 0
        print("clear")
        pixels.set_pixel_all((0, 1, 0))
        pixels.show()
    return offset


def channelcheck_update(offset):
    """Channel check."""
    # print("offset", offset)

    pixels.set_channel(offset, VALUE_HIGH)
    # clear last set channel
    last = offset - 1
    if last < 0:
        last = pixels.channel_count - 1
    pixels.set_channel(last, 0)
    pixels.show()

    offset += 1
    if offset >= pixels.channel_count:
        offset = 0
        print("offset overflow. start from 0")
    return offset


##########################################


def timeit_call(message, test_function, loop_count=1000):
    """Measure timing."""
    duration = 0
    start_time = time.monotonic()
    for _index in range(loop_count):
        start_time = time.monotonic()
        test_function()
        end_time = time.monotonic()
        duration += end_time - start_time
    # print(
    #     "duration:\n"
    #     "\t{}s for {} loops\n"
    #     "\t{:.2f}ms per call"
    #     "".format(
    #         duration,
    #         loop_count,
    #         (duration/loop_count)*1000
    #     )
    # )
    # print(
    #     "\t{:.2f}ms per call"
    #     "".format((duration / loop_count) * 1000)
    # )
    # "{:>8.2f}ms".format(3.56)
    print(
        "{call_duration:>10.4f}ms\t{message}"
        "".format(
            call_duration=(duration / loop_count) * 1000,
            message=message,
        )
    )


def timeit_pixels_show():
    """Measure timing."""
    print("*** pixels show:")
    loop_count = 1000

    def _test():
        pixels.show()

    timeit_call("'pixels.show()'", _test, loop_count)


def timeit_pixels_set_single():
    """Measure timing pixels set."""
    print("*** pixels set single:")
    loop_count = 1000

    def _test():
        pixels[3] = (500, 40500, 1000)

    timeit_call("'pixels[3] = (500, 40500, 1000)'", _test, loop_count)

    def _test():
        pixels[3] = (0.1, 0.5, 0.9)

    timeit_call("'pixels[3] = (0.1, 0.5, 0.9)'", _test, loop_count)

    def _test():
        pixels.set_pixel(3, (500, 40500, 1000))

    timeit_call("'pixels.set_pixel(3, (500, 40500, 1000))'", _test, loop_count)

    def _test():
        pixels.set_pixel(3, (0.1, 0.5, 0.9))

    timeit_call("'pixels.set_pixel(3, (0.1, 0.5, 0.9))'", _test, loop_count)


def timeit_pixels_set_loop():
    """Measure timing pixels set."""
    print("*** pixels set loop:")
    loop_count = 10

    def _test():
        for i in range(PIXEL_COUNT):
            pixels[i] = (500, 40500, 1000)

    timeit_call(
        "'pixels[0..{}] = (500, 40500, 1000)'".format(PIXEL_COUNT), _test, loop_count
    )

    def _test():
        for i in range(PIXEL_COUNT):
            pixels[i] = (0.1, 0.5, 0.9)

    timeit_call(
        "'pixels[0..{}] = (0.1, 0.5, 0.9)'".format(PIXEL_COUNT), _test, loop_count
    )

    def _test():
        for i in range(PIXEL_COUNT):
            pixels.set_pixel(i, (500, 40500, 1000))

    timeit_call(
        "'pixels.set_pixel(0..{}, (500, 40500, 1000))'".format(PIXEL_COUNT),
        _test,
        loop_count,
    )

    def _test():
        for i in range(PIXEL_COUNT):
            pixels.set_pixel(i, (0.1, 0.5, 0.9))

    timeit_call(
        "'pixels.set_pixel(0..{}, (0.1, 0.5, 0.9))'".format(PIXEL_COUNT),
        _test,
        loop_count,
    )


def timeit_pixels_set_all():
    """Measure timing pixels set."""
    print("*** pixels set all:")
    loop_count = 10

    def _test():
        pixels.set_pixel_all((500, 40500, 1000))

    timeit_call("'pixels.set_pixel_all((500, 40500, 1000))'", _test, loop_count)

    def _test():
        pixels.set_pixel_all((0.1, 0.5, 0.9))

    timeit_call("'pixels.set_pixel_all((0.1, 0.5, 0.9))'", _test, loop_count)

    def _test():
        pixels.set_pixel_all_16bit_value(500, 40500, 1000)

    timeit_call(
        "'pixels.set_pixel_all_16bit_value(500, 40500, 1000)'", _test, loop_count
    )

    def _test():
        pixels.set_all_black()

    timeit_call("'pixels.set_all_black()'", _test, loop_count)


def timeit_pixels_set_16bit():
    """Measure timing pixels set."""
    print("*** pixels set 16bit:")
    loop_count = 1000

    def _test():
        pixels.set_pixel_16bit_value(3, 500, 40500, 1000)

    timeit_call(
        "'pixels.set_pixel_16bit_value(3, 500, 40500, 1000)'", _test, loop_count
    )

    def _test():
        pixels.set_pixel_16bit_color(3, (500, 40500, 1000))

    timeit_call(
        "'pixels.set_pixel_16bit_color(3, (500, 40500, 1000))'", _test, loop_count
    )

    def _test():
        for i in range(PIXEL_COUNT):
            pixels.set_pixel_16bit_value(i, 500, 40500, 1000)

    timeit_call(
        "'pixels.set_pixel_16bit_value(0..{}, 500, 40500, 1000)'"
        "".format(PIXEL_COUNT),
        _test,
        10,
    )

    def _test():
        for i in range(PIXEL_COUNT):
            pixels.set_pixel_16bit_color(i, (500, 40500, 1000))

    timeit_call(
        "'pixels.set_pixel_16bit_color(0..{}, (500, 40500, 1000))'"
        "".format(PIXEL_COUNT),
        _test,
        10,
    )


def timeit_pixels_set_float():
    """Measure timing pixels set."""
    print("*** pixels set float:")
    loop_count = 1000

    def _test():
        pixels.set_pixel_float_value(3, 0.1, 0.5, 0.9)

    timeit_call("'pixels.set_pixel_float_value(3, 0.1, 0.5, 0.9)'", _test, loop_count)

    def _test():
        pixels.set_pixel_float_color(3, (0.1, 0.5, 0.9))

    timeit_call("'pixels.set_pixel_float_color(3, (0.1, 0.5, 0.9))'", _test, loop_count)

    def _test():
        for i in range(PIXEL_COUNT):
            pixels.set_pixel_float_value(i, 0.1, 0.5, 0.9)

    timeit_call(
        "'pixels.set_pixel_float_value(0..{}, 0.1, 0.5, 0.9)'" "".format(PIXEL_COUNT),
        _test,
        10,
    )

    def _test():
        for i in range(PIXEL_COUNT):
            pixels.set_pixel_float_color(i, (0.1, 0.5, 0.9))

    timeit_call(
        "'pixels.set_pixel_float_color(0..{}, (0.1, 0.5, 0.9))'" "".format(PIXEL_COUNT),
        _test,
        10,
    )

    def _test():
        for i in range(PIXEL_COUNT):
            pixels.set_pixel_16bit_value(
                i, int(0.1 * 65535), int(0.5 * 65535), int(0.9 * 65535)
            )

    timeit_call(
        "'pixels.set_pixel_16bit_value(0..{}, f2i 0.1, f2i 0.5, f2i 0.9)'"
        "".format(PIXEL_COUNT),
        _test,
        10,
    )


def timeit_channel_set():
    """Measure timing channel set."""
    print("*** channel set:")
    loop_count = 1000

    def _test():
        pixels.set_channel(0, 10000)

    timeit_call("'set_channel(0, 10000)'", _test, loop_count)

    def _test():
        pixels.set_channel(0, 10000)
        pixels.set_channel(1, 10000)
        pixels.set_channel(2, 10000)

    timeit_call("'set_channel(0..2, 10000)'", _test, loop_count)

    channel_count = PIXEL_COUNT * 3

    def _test():
        for i in range(channel_count):
            pixels.set_channel(i, 500)

    timeit_call("'set_channel(for 0..{}, 10000)'" "".format(channel_count), _test, 10)


def timeit_channel_set_internal():
    """Measure timing channel set internal."""
    print("*** channel set internal:")
    # loop_count = 1000
    #
    # def _test():
    #     pixels._set_channel_16bit_value(0, 10000)
    # timeit_call(
    #     "'_set_channel_16bit_value(0, 10000)'",
    #     _test,
    #     loop_count
    # )
    #
    # def _test():
    #     pixels._set_channel_16bit_value(0, 10000)
    #     pixels._set_channel_16bit_value(1, 10000)
    #     pixels._set_channel_16bit_value(2, 10000)
    # timeit_call(
    #     "'_set_channel_16bit_value(0..2, 10000)'",
    #     _test,
    #     loop_count
    # )
    #
    # def _test():
    #     for i in range(PIXEL_COUNT * 3):
    #         pixels._set_channel_16bit_value(i, 500)
    # timeit_call(
    #     "'_set_channel_16bit_value(for 0..{}, 10000)'"
    #     "".format(PIXEL_COUNT * 3),
    #     _test,
    #     10
    # )
    print("    must be uncommented in code to work..")


def timeit_pixels_get():
    """Measure timing pixels get."""
    print("*** pixels get:")

    pixels.set_pixel_all((1, 11, 111))

    def _test():
        print("[", end="")
        for i in range(PIXEL_COUNT):
            print("{}:{}, ".format(i, pixels[i]), end="")
        print("]")

    timeit_call("'print('{}:{}, '.format(i, pixels[i]), end='')'", _test, 1)


def time_measurement():
    """Measure timing."""
    print("meassure timing:")
    timeit_pixels_show()
    timeit_pixels_set_single()
    timeit_pixels_set_loop()
    timeit_pixels_set_all()
    timeit_pixels_set_16bit()
    timeit_pixels_set_float()
    timeit_channel_set()
    timeit_channel_set_internal()
    timeit_pixels_get()
    pixels.set_pixel_all((0, 1, 1))


##########################################


def test_bcdata():
    """Test BC-Data setting."""
    print("test BC-Data setting:")
    print("set pixel all to 100, 100, 100")
    pixels.set_pixel_all((100, 100, 100))
    pixels.show()
    time.sleep(2)
    print(
        "bcr: {:>3}\n"
        "bcg: {:>3}\n"
        "bcb: {:>3}\n"
        "".format(
            pixels.bcr,
            pixels.bcg,
            pixels.bcb,
        )
    )
    # calculate bc values
    Ioclmax = adafruit_tlc59711.TLC59711.calculate_Ioclmax(Riref=2.7)
    print("Ioclmax = {}".format(Ioclmax))
    Riref = adafruit_tlc59711.TLC59711.calculate_Riref(Ioclmax=Ioclmax)
    print("Riref = {}".format(Riref))
    BCValues = adafruit_tlc59711.TLC59711.calculate_BCData(
        Ioclmax=Ioclmax,
        IoutR=18,
        IoutG=11,
        IoutB=13,
    )
    # (127, 77, 91)
    print("BCValues = {}".format(BCValues))

    print("set bcX")
    pixels.bcr = BCValues[0]
    pixels.bcg = BCValues[1]
    pixels.bcb = BCValues[2]
    pixels.update_BCData()
    pixels.show()
    print(
        "bcr: {:>3}\n"
        "bcg: {:>3}\n"
        "bcb: {:>3}\n"
        "".format(
            pixels.bcr,
            pixels.bcg,
            pixels.bcb,
        )
    )
    time.sleep(2)


##########################################


def test_main():
    """Test Main."""
    print(42 * "*", end="")
    print(__doc__, end="")
    print(42 * "*")
    # print()
    # time.sleep(0.5)
    # print(42 * '*')

    pixels.set_pixel_all_16bit_value(1, 10, 100)
    pixels.show()
    time.sleep(0.5)

    test_bcdata()
    time.sleep(0.5)
    print(42 * "*")

    time_measurement()
    time.sleep(0.5)
    print(42 * "*")

    offset = 0

    print("loop:")
    while True:
        offset = channelcheck_update(offset)
        time.sleep(0.5)
        print(offset)


##########################################
# main loop

if __name__ == "__main__":
    test_main()
