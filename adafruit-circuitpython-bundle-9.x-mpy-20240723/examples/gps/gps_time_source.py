# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple script using GPS timestamps as RTC time source
# The GPS timestamps are available without a fix and keep the track of
# time while there is powersource (ie coin cell battery)

import time
import board
import busio
import rtc
import adafruit_gps

uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=10)
# i2c = busio.I2C(board.SCL, board.SDA)

gps = adafruit_gps.GPS(uart, debug=False)
# gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)  # Use I2C interface

gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
gps.send_command(b"PMTK220,1000")

print("Set GPS as time source")
rtc.set_time_source(gps)
the_rtc = rtc.RTC()


def _format_datetime(datetime):
    return "{:02}/{:02}/{} {:02}:{:02}:{:02}".format(
        datetime.tm_mon,
        datetime.tm_mday,
        datetime.tm_year,
        datetime.tm_hour,
        datetime.tm_min,
        datetime.tm_sec,
    )


last_print = time.monotonic()
while True:
    gps.update()
    # Every second print out current time from GPS, RTC and time.localtime()
    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current
        if not gps.timestamp_utc:
            print("No time data from GPS yet")
            continue
        # Time & date from GPS informations
        print("Fix timestamp: {}".format(_format_datetime(gps.timestamp_utc)))

        # Time & date from internal RTC
        print("RTC timestamp: {}".format(_format_datetime(the_rtc.datetime)))

        # Time & date from time.localtime() function
        local_time = time.localtime()

        print("Local time: {}".format(_format_datetime(local_time)))
