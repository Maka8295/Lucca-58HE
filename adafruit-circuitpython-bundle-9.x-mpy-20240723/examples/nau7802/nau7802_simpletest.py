# SPDX-FileCopyrightText: 2023 Cedar Grove Maker Studios
# SPDX-License-Identifier: MIT

"""
nau7802_simpletest.py  2023-01-13 2.0.2  Cedar Grove Maker Studios

Instantiates two NAU7802 channels with default gain of 128 and sample
average count of 2.
"""

import time
import board
from cedargrove_nau7802 import NAU7802

# Instantiate 24-bit load sensor ADC; two channels, default gain of 128
nau7802 = NAU7802(board.I2C(), address=0x2A, active_channels=2)


def zero_channel():
    """Initiate internal calibration for current channel.Use when scale is started,
    a new channel is selected, or to adjust for measurement drift. Remove weight
    and tare from load cell before executing."""
    print(
        "channel %1d calibrate.INTERNAL: %5s"
        % (nau7802.channel, nau7802.calibrate("INTERNAL"))
    )
    print(
        "channel %1d calibrate.OFFSET:   %5s"
        % (nau7802.channel, nau7802.calibrate("OFFSET"))
    )
    print("...channel %1d zeroed" % nau7802.channel)


def read_raw_value(samples=2):
    """Read and average consecutive raw sample values. Return average raw value."""
    sample_sum = 0
    sample_count = samples
    while sample_count > 0:
        while not nau7802.available():
            pass
        sample_sum = sample_sum + nau7802.read()
        sample_count -= 1
    return int(sample_sum / samples)


# Instantiate and calibrate load cell inputs
print("*** Instantiate and calibrate load cells")
# Enable NAU7802 digital and analog power
enabled = nau7802.enable(True)
print("Digital and analog power enabled:", enabled)

print("REMOVE WEIGHTS FROM LOAD CELLS")
time.sleep(3)

nau7802.channel = 1
zero_channel()  # Calibrate and zero channel
nau7802.channel = 2
zero_channel()  # Calibrate and zero channel

print("READY")

### Main loop: Read load cells and display raw values
while True:
    print("=====")
    nau7802.channel = 1
    value = read_raw_value()
    print("channel %1.0f raw value: %7.0f" % (nau7802.channel, value))

    nau7802.channel = 2
    value = read_raw_value()
    print("channel %1.0f raw value: %7.0f" % (nau7802.channel, value))
