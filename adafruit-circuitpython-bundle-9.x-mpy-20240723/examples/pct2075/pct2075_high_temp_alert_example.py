# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_pct2075

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
pct = adafruit_pct2075.PCT2075(i2c)

pct.high_temperature_threshold = 35.5
pct.temperature_hysteresis = 30.0
pct.high_temp_active_high = False
print("High temp alert active high? %s" % pct.high_temp_active_high)

# Attach an LED with the Cathode to the INT pin and Anode to 3.3V with a current limiting resistor

while True:
    print("Temperature: %.2f C" % pct.temperature)
    time.sleep(0.5)
