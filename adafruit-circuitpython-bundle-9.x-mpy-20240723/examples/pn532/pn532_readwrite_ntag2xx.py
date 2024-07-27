# SPDX-FileCopyrightText: 2015 Tony DiCola and Roberto Laricchia for Adafruit Industries
# SPDX-License-Identifier: MIT

# Example of detecting and reading a block from a MiFare NFC card.

"""
This example shows connecting to the PN532 and writing & reading an ntag2xx
type RFID tag
"""

import board
import busio
from digitalio import DigitalInOut

#
# NOTE: pick the import that matches the interface being used
#
# from adafruit_pn532.i2c import PN532_I2C
from adafruit_pn532.spi import PN532_SPI

# from adafruit_pn532.uart import PN532_UART

# I2C connection:
# i2c = busio.I2C(board.SCL, board.SDA)

# Non-hardware reset/request with I2C
# pn532 = PN532_I2C(i2c, debug=False)

# With I2C, we recommend connecting RSTPD_N (reset) to a digital pin for manual
# harware reset
# reset_pin = DigitalInOut(board.D6)
# On Raspberry Pi, you must also connect a pin to P32 "H_Request" for hardware
# wakeup! this means we don't need to do the I2C clock-stretch thing
# req_pin = DigitalInOut(board.D12)
# pn532 = PN532_I2C(i2c, debug=False, reset=reset_pin, req=req_pin)

# SPI connection:
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D5)
pn532 = PN532_SPI(spi, cs_pin, debug=False)

# UART connection
# uart = busio.UART(board.TX, board.RX, baudrate=115200, timeout=0.1)
# pn532 = PN532_UART(uart, debug=False)

ic, ver, rev, support = pn532.firmware_version
print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

print("Waiting for RFID/NFC card to write to!")
while True:
    # Check if a card is available to read
    uid = pn532.read_passive_target(timeout=0.5)
    print(".", end="")
    # Try again if no card is available.
    if uid is not None:
        break

print("")
print("Found card with UID:", [hex(i) for i in uid])

# Set 4 bytes of block to 0xFEEDBEEF
data = bytearray(4)
data[0:4] = b"\xFE\xED\xBE\xEF"
# Write 4 byte block.
pn532.ntag2xx_write_block(6, data)
# Read block #6
ntag2xx_block = pn532.ntag2xx_read_block(6)
if ntag2xx_block is not None:
    print(
        "Wrote to block 6, now trying to read that data:",
        [hex(x) for x in ntag2xx_block],
    )
else:
    print("Read failed - did you remove the card?")
