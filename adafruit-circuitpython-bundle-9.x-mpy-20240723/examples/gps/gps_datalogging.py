# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple GPS datalogging demonstration.
# This example uses the GPS library and to read raw NMEA sentences
# over I2C or UART from the GPS unit and dumps them to a file on an SD card
# (recommended), microcontroller internal storage (be careful as only a few
# kilobytes are available), or to a filesystem.
# If you are using a microcontroller, before writing to internal storage you
#  MUST carefully follow the steps in this guide to enable writes to the
# internal filesystem:
#  https://learn.adafruit.com/adafruit-ultimate-gps-featherwing/circuitpython-library
import sys

import board
import busio
import adafruit_gps

# Path to the file to log GPS data.  By default this will be appended to
# which means new lines are added at the end and all old data is kept.
# Change this path to point at internal storage (like '/gps.txt') or SD
# card mounted storage ('/sd/gps.txt') as desired.
LOG_FILE = "gps.txt"  # Example for writing to internal path gps.txt

# File more for opening the log file.  Mode 'ab' means append or add new lines
# to the end of the file rather than erasing it and starting over.  If you'd
# like to erase the file and start clean each time use the value 'wb' instead.
LOG_MODE = "ab"

# sdcardio and adafruit_sdcard are NOT supported on blinka. If you are using a
# Raspberry Pi or other single-board linux computer, the code will save the
# output to the path defined in LOG_FILE above.
if sys.platform != "linux":
    import storage

    SD_CS_PIN = board.D10  # CS for SD card using Adalogger Featherwing
    try:
        import sdcardio

        sdcard = sdcardio.SDCard(board.SPI, SD_CS_PIN)
    except ImportError:
        import adafruit_sdcard
        import digitalio

        sdcard = adafruit_sdcard.SDCard(
            board.SPI(),
            digitalio.DigitalInOut(SD_CS_PIN),
        )

    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")  # Mount SD card under '/sd' path in filesystem.
    LOG_FILE = "/sd/gps.txt"  # Example for writing to SD card path /sd/gps.txt

# Create a serial connection for the GPS connection using default speed and
# a slightly higher timeout (GPS modules typically update once a second).
# These are the defaults you should use for the GPS FeatherWing.
# For other boards set RX = GPS module TX, and TX = GPS module RX pins.
uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=10)

# If using a USB/Serial converter, use pyserial and update the serial
# port name to match the serial connection for the GPS!
# import serial
# uart = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=10)

# If using I2C, we'll create an I2C interface to talk to using default pins
# i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

# Create a GPS module instance.
gps = adafruit_gps.GPS(uart)  # Use UART/pyserial
# gps = adafruit_gps.GPS_GtopI2C(i2c)  # Use I2C interface

# Main loop just reads data from the GPS module and writes it back out to
# the output file while also printing to serial output.
with open(LOG_FILE, LOG_MODE) as outfile:
    while True:
        sentence = gps.readline()
        if not sentence:
            continue
        print(str(sentence, "ascii").strip())
        outfile.write(sentence)
        outfile.flush()
