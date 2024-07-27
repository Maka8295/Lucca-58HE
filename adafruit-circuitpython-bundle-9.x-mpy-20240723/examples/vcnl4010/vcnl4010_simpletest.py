# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of the VCNL4010 proximity and light sensor.
# Will print the proximity and ambient light every second.
import time
import board
import adafruit_vcnl4010


i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = adafruit_vcnl4010.VCNL4010(i2c)

# You can optionally adjust the sensor LED current.  The default is 200mA
# which is the maximum value.  Note this is only set in 10mA increments.
# sensor.led_current_mA = 120  # Set 120 mA LED current

# You can also adjust the measurement frequency for the sensor.  The default
# is 390.625 khz, but these values are possible to set too:
# - FREQUENCY_3M125: 3.125 Mhz
# - FREQUENCY_1M5625: 1.5625 Mhz
# - FREQUENCY_781K25: 781.25 Khz
# - FREQUENCY_390K625: 390.625 Khz (default)
# sensor.frequency = adafruit_vcnl4010.FREQUENCY_3M125  # 3.125 Mhz

# Main loop runs forever printing the proximity and light level.
while True:
    proximity = sensor.proximity  # Proximity has no units and is a 16-bit
    # value.  The LOWER the value the further
    # an object from the sensor (up to ~200mm).
    print("Proximity: {0}".format(proximity))
    ambient_lux = sensor.ambient_lux
    print("Ambient light: {0} lux".format(ambient_lux))
    time.sleep(1.0)
