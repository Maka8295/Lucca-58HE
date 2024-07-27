# SPDX-FileCopyrightText: 2022 wrdaigle for Adafruit Industries
# SPDX-FileCopyrightText: 2022 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
VL53L4CD multiple sensor I2C set_address demo.

This example is written for two sensors, but it can easily be modified to include more.

NOTE: A multitude of sensors may require more current than the on-board 3V regulator can output.
The typical current consumption during active range readings is about 19 mA per sensor.
"""

import time
import board
import digitalio
import adafruit_vl53l4cd

# Define the I2C pins.
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

xshut = [
    # Update the D6 and D5 pins to match the pins to which you wired your sensor XSHUT pins.
    digitalio.DigitalInOut(board.D6),
    digitalio.DigitalInOut(board.D5),
    # Add more VL53L4CD sensors by defining their XSHUT pins here.
]

for shutdown_pin in xshut:
    # Set the shutdown pins to output, and pull them low.
    shutdown_pin.switch_to_output(value=False)
    # These pins are active when Low, meaning:
    #   If the output signal is LOW, then the VL53L4CD sensor is off.
    #   If the output signal is HIGH, then the VL53L4CD sensor is on.
# All VL53L4CD sensors are now off.

# Create a list to be used for the array of VL53L4CD sensors.
vl53l4cd_list = []

# Change the address of the additional VL53L4CD sensors.
for pin_number, shutdown_pin in enumerate(xshut):
    # Turn on the VL53L4CD sensors to allow hardware check.
    shutdown_pin.value = True
    # Instantiate the VL53L4CD I2C object and insert it into the VL53L4CD list.
    # This also performs VL53L4CD hardware check.
    sensor_i2c = adafruit_vl53l4cd.VL53L4CD(i2c)
    vl53l4cd_list.append(sensor_i2c)
    # This ensures no address change on one sensor board, specifically the last one in the series.
    if pin_number < len(xshut) - 1:
        # The default address is 0x29. Update it to an address that is not already in use.
        sensor_i2c.set_address(pin_number + 0x30)

# Print the various sensor I2C addresses to the serial console.
if i2c.try_lock():
    print("Sensor I2C addresses:", [hex(x) for x in i2c.scan()])
    i2c.unlock()

# Start ranging for sensor data collection.
for sensor in vl53l4cd_list:
    sensor.start_ranging()
while True:
    # Extract the appropriate data from the current list, and print
    # the sensor distance readings for all available sensors.
    for sensor_number, sensor in enumerate(vl53l4cd_list):
        if sensor.data_ready:
            print("Sensor {}: {}".format(sensor_number + 1, sensor.distance))
            sensor.clear_interrupt()
    time.sleep(0.5)
