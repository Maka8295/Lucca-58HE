# SPDX-FileCopyrightText: 2021 Jose David M
#
# SPDX-License-Identifier: Unlicense
"""
Example showing the use of Fake_requests to access a Temperature Sensor information
Database. Inspired on the I2C buddy and a Discussion with Hugo Dahl
"""
import board
from adafruit_fakerequests import Fake_Requests

# Create the fakerequest request and get the temperature sensor definitions
# It will look through the database and print the name of the sensor and
# the temperature
response = Fake_Requests("fakerequests_i2c_database.txt")
definitions = response.text.split("\n")

# We create the i2c object and set a flag to let us know if the sensor is found
found = False
i2c = board.I2C()

# We look for all the sensor address and added to a list
print("Looking for addresses")
i2c.unlock()  # used here, to avoid problems with the I2C bus
i2c.try_lock()
sensor_address = int(i2c.scan()[-1])
print("Sensor address is:", hex(sensor_address))
i2c.unlock()  # unlock the bus

# Create an empty list for the sensors found in the database
sensor_choices = []

# Compare the sensor found vs the database. this is done because
# we could have the case that the same address corresponds to
# two or more temperature sensors
for sensor in definitions:
    elements = sensor.split(",")
    if int(elements[0]) == sensor_address:
        sensor_choices.append(sensor)

# This is the main logic to found the sensor and try to
# initiate it. It would raise some exceptions depending
# on the situation. As an example this is not perfect
# and only serves to show the library capabilities
# and nothing more
for find_sensor in sensor_choices:
    module = find_sensor.split(",")
    package = module[2]
    class_name = str(module[3]).strip(" ")
    try:
        module = __import__(package)
        variable = getattr(module, class_name)
        try:
            sensor = variable(i2c)
            print(
                "The sensor {} gives a temperature of {} Celsius".format(
                    class_name, sensor.temperature
                )
            )
            found = True
        except ValueError:
            pass
    except Exception as e:
        raise ImportError(
            "Could not find the module {} in your lib folder.".format(package)
        ) from e

if found:
    print("Congratulations")
else:
    print("We could not find a valid Temperature Sensor")
