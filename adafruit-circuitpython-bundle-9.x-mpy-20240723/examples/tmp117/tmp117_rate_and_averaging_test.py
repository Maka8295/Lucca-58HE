# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
# pylint:disable=no-member

# This example is best viewed using a serial plotter
# such as the one built into the Mu editor.
import time
import board
from adafruit_tmp117 import TMP117, AverageCount, MeasurementDelay

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
tmp117 = TMP117(i2c)

# uncomment different options below to see how it affects the reported temperature
# tmp117.averaged_measurements = AverageCount.AVERAGE_1X
# tmp117.averaged_measurements = AverageCount.AVERAGE_8X
# tmp117.averaged_measurements = AverageCount.AVERAGE_32X
# tmp117.averaged_measurements = AverageCount.AVERAGE_64X

# tmp117.measurement_delay = MeasurementDelay.DELAY_0_0015_S
# tmp117.measurement_delay = MeasurementDelay.DELAY_0_125_S
# tmp117.measurement_delay = MeasurementDelay.DELAY_0_250_S
# tmp117.measurement_delay = MeasurementDelay.DELAY_0_500_S
# tmp117.measurement_delay = MeasurementDelay.DELAY_1_S
# tmp117.measurement_delay = MeasurementDelay.DELAY_4_S
# tmp117.measurement_delay = MeasurementDelay.DELAY_8_S
# tmp117.measurement_delay = MeasurementDelay.DELAY_16_S

print(
    "Number of averaged samples per measurement:",
    AverageCount.string[tmp117.averaged_measurements],
)
print(
    "Minimum time between measurements:",
    MeasurementDelay.string[tmp117.measurement_delay],
    "seconds",
)
print("")

while True:
    print("Temperature:", tmp117.temperature)
    time.sleep(0.01)
