# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple seesaw test reading and writing the internal EEPROM
# The ATtiny8xx series has a true 128 byte EEPROM, the SAMD09 mimics it in flash with 64 bytes
# THE LAST BYTE IS USED FOR I2C ADDRESS CHANGE!

import time
import board
from adafruit_seesaw import seesaw

i2c_bus = board.I2C()  # uses board.SCL and board.SDA
# i2c_bus = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
ss = seesaw.Seesaw(i2c_bus)

value = ss.eeprom_read8(0x02)  # Read from address 2
print("Read 0x%02x from EEPROM address 0x02" % value)

print("Incrementing value")
ss.eeprom_write8(0x02, (value + 1) % 0xFF)

value = ss.eeprom_read8(0x02)  # Read from address 2
print("Second read 0x%02x from EEPROM address 0x02" % value)

while True:
    # Do not write EEPROM in a loop, it has 100k cycle life
    time.sleep(1)
