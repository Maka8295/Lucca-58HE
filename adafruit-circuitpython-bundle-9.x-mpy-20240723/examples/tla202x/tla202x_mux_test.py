# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
# pylint:disable=no-member
import board
import busio
from adafruit_tla202x import TLA2024, Mux

i2c = busio.I2C(board.SCL, board.SDA)
tla = TLA2024(i2c)

for i in range(4):
    channel = i
    tla.input_channel = channel
    print("Channel", channel, ":", tla.voltage)

muxen = [
    [Mux.MUX_AIN0_GND, 0.5],
    [Mux.MUX_AIN1_GND, 1.0],
    [Mux.MUX_AIN2_GND, 0.0],
    [Mux.MUX_AIN3_GND, 2.0],
    [Mux.MUX_AIN0_AIN1, None],
    [Mux.MUX_AIN0_AIN3, None],
    [Mux.MUX_AIN1_AIN3, None],
    [Mux.MUX_AIN2_AIN3, None],
]
muxen[-4][1] = muxen[0][1] - muxen[1][1]
muxen[-3][1] = muxen[0][1] - muxen[3][1]
muxen[-2][1] = muxen[1][1] - muxen[3][1]
muxen[-1][1] = muxen[2][1] - muxen[3][1]
for mux, ev in muxen:
    tla.mux = mux
    name = Mux.string[mux]
    actual = tla.voltage
    delta = abs(ev - actual)

    if delta <= 0.01:
        result = "PASSED!"
    else:
        result = "FAIL :("
    print(
        "Mux: %s\tEV: %3f\tActual: %3f\tDelta: %5f\t%s"
        % (name, ev, actual, delta, result)
    )
