# SPDX-FileCopyrightText: Copyright (c) 2023 Liz Clark for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
Simple test for the HUSB238.
Reads available voltages and then sets each available voltage.
Reads the set voltage and current from the attached PD power supply.
"""
import time
import board
import adafruit_husb238

i2c = board.I2C()

# Initialize HUSB238
pd = adafruit_husb238.Adafruit_HUSB238(i2c)
voltages = pd.available_voltages
print("The following voltages are available:")
for i, volts in enumerate(voltages):
    print(f"{volts}V")

v = 0

while True:
    while pd.attached:
        print(f"Setting to {voltages[v]}V!")
        pd.voltage = voltages[v]
        print(f"It is set to {pd.voltage}V/{pd.current}A")
        print()
        v = (v + 1) % len(voltages)
        time.sleep(2)
