# SPDX-FileCopyrightText: 2018 Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2018 Walter Haschka
# SPDX-License-Identifier: MIT

# Simple demo of controlling a chain of several TLC5947 12-bit 24-channel PWM controllers.
# Will update channel values to different PWM duty cycles.
# Authors: Tony DiCola, Walter Haschka

import board
import busio
import digitalio

import adafruit_tlc5947

# Initialize SPI bus.
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)

# Initialize TLC5947
DRIVER_COUNT = 2  # change this to the number of drivers you have chained
LATCH = digitalio.DigitalInOut(board.D5)
tlc5947 = adafruit_tlc5947.TLC5947(spi, LATCH, num_drivers=DRIVER_COUNT)

# You can optionally disable auto_write which allows you to control when
# channel state is written to the chip.  Normally auto_write is true and
# will automatically write out changes as soon as they happen to a channel, but
# if you need more control or atomic updates of multiple channels then disable
# and manually call write as shown below.
# tlc5947 = adafruit_tlc5947.TLC5947(spi, LATCH, num_drivers=DRIVER_COUNT, auto_write=False)

# There are two ways to set channel PWM values. The first is by getting
# a PWMOut object that acts like the built-in PWMOut and can be used anywhere
# it is used in your code.  Change the duty_cycle property to a 16-bit value
# (note this is NOT the 12-bit value supported by the chip natively) and the
# PWM channel will be updated.


def first_last():
    """Cycles the red pin of LED one up, then the other LED; now dims the LEDs
    both down. Repeats with green and blue pins. Then starts all over again.

    Hook up one RGB LED to pins 0 (red), 1 (green), and 2 (blue), AND connect
    another RGB LED to pins 21, 22 and 23 of the last chained driver, respectively.
    """
    redA = tlc5947.create_pwm_out(0)
    greenA = tlc5947.create_pwm_out(1)
    blueA = tlc5947.create_pwm_out(2)
    redZ = tlc5947.create_pwm_out(DRIVER_COUNT * 24 - 3)
    greenZ = tlc5947.create_pwm_out(DRIVER_COUNT * 24 - 2)
    blueZ = tlc5947.create_pwm_out(DRIVER_COUNT * 24 - 1)

    step = 10
    start_pwm = 0
    end_pwm = 32767  # 50% (32767, or half of the maximum 65535):

    while True:
        for pinA, pinZ in ((redA, redZ), (greenA, greenZ), (blueA, blueZ)):
            # Brighten:
            print("LED A up")
            for pwm in range(start_pwm, end_pwm, step):
                pinA.duty_cycle = pwm
                # tlc5947.write()        # see NOTE below

            print("LED Z up")
            for pwm in range(start_pwm, end_pwm, step):
                pinZ.duty_cycle = pwm
                # tlc5947.write()        # see NOTE below

            # Dim:
            print("LED A and LED Z down")
            for pwm in range(end_pwm, start_pwm, 0 - step):
                pinA.duty_cycle = pwm
                pinZ.duty_cycle = pwm
                # tlc5947.write()        # see NOTE below

    # NOTE: if auto_write was disabled you need to call write on the parent to
    # make sure the value is written in each loop (this is not common, if disabling
    # auto_write you probably want to use the direct 12-bit raw access instead,
    # shown next).


# ----------
# The other way to read and write channels is directly with each channel 12-bit
# value and an item accessor syntax.  Index into the TLC5947 with the channel
# number (0-max) and get or set its 12-bit value (0-4095).
def test_all_channels(step):
    """Loops over all available channels of all connected driver boards,
    brightening and dimming all LEDs one after the other. With RGB LEDs,
    all each component is cycled. Repeats forever.

    :param step: the PWM increment in each cycle. Higher values makes cycling quicker.
    """

    start_pwm = 0
    end_pwm = 3072  # 75% of the maximum 4095

    while True:
        for pin in range(DRIVER_COUNT * 24):
            # Brighten:
            for pwm in range(start_pwm, end_pwm, step):
                tlc5947[pin] = pwm
                # Again be sure to call write if you disabled auto_write.
                # tlc5947.write()

            # Dim:
            for pwm in range(end_pwm, start_pwm, 0 - step):
                tlc5947[pin] = pwm
                # Again be sure to call write if you disabled auto_write.
                # tlc5947.write()


# ----------
# Choose here which function to try:
# first_last()
test_all_channels(16)
