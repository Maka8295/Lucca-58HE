# SPDX-FileCopyrightText: 2020 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board

# for I2C use:
from adafruit_as726x import AS726x_I2C

# for UART use:
# from adafruit_as726x import AS726x_UART

# maximum value for sensor reading
max_val = 16000

# max number of characters in each graph
max_graph = 80


def graph_map(x):
    return min(int(x * max_graph / max_val), max_graph)


# for I2C use:
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = AS726x_I2C(i2c)

# for UART use:
# uart = board.UART()
# sensor = AS726x_UART(uart)

sensor.conversion_mode = sensor.MODE_2

while True:
    # Wait for data to be ready
    while not sensor.data_ready:
        time.sleep(0.1)

    # plot plot the data
    print("\n")
    print("V: " + graph_map(sensor.violet) * "=")
    print("B: " + graph_map(sensor.blue) * "=")
    print("G: " + graph_map(sensor.green) * "=")
    print("Y: " + graph_map(sensor.yellow) * "=")
    print("O: " + graph_map(sensor.orange) * "=")
    print("R: " + graph_map(sensor.red) * "=")

    time.sleep(1)
