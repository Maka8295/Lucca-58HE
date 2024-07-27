# SPDX-FileCopyrightText: 2021 lesamouraipourpre
# SPDX-License-Identifier: MIT

# This example uses GSA and GSV sentences from the GPS device to report on the
# quality of the received data from the satellites.
# * GSA - DOP(Dilution of Precision) and active satellites
# * GSV - Satellites in view

import time
import board

import adafruit_gps

# Create a serial connection for the GPS connection using default speed and
# a slightly higher timeout (GPS modules typically update once a second).
# These are the defaults you should use for the GPS FeatherWing.
# For other boards set RX = GPS module TX, and TX = GPS module RX pins.
# import busio
# uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=10)

# for a computer, use the pyserial library for uart access
# import serial
# uart = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=10)

# If using I2C, we'll create an I2C interface to talk to using default pins
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

# Create a GPS module instance.
# gps = adafruit_gps.GPS(uart, debug=False)  # Use UART/pyserial
gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)  # Use I2C interface

# Initialize the GPS module by changing what data it sends and at what rate.
# These are NMEA extensions for PMTK_314_SET_NMEA_OUTPUT and
# PMTK_220_SET_NMEA_UPDATERATE but you can send anything from here to adjust
# the GPS module behavior:
#   https://cdn-shop.adafruit.com/datasheets/PMTK_A11.pdf

# Turn on everything (not all of it is parsed!)
gps.send_command(b"PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0")

# Set update rate to once a second (1hz) which is what you typically want.
gps.send_command(b"PMTK220,1000")
# Or decrease to once every two seconds by doubling the millisecond value.
# Be sure to also increase your UART timeout above!
# gps.send_command(b'PMTK220,2000')
# You can also speed up the rate, but don't go too fast or else you can lose
# data during parsing.  This would be twice a second (2hz, 500ms delay):
# gps.send_command(b'PMTK220,500')


def format_dop(dop):
    # https://en.wikipedia.org/wiki/Dilution_of_precision_(navigation)
    if dop > 20:
        msg = "Poor"
    elif dop > 10:
        msg = "Fair"
    elif dop > 5:
        msg = "Moderate"
    elif dop > 2:
        msg = "Good"
    elif dop > 1:
        msg = "Excellent"
    else:
        msg = "Ideal"
    return f"{dop} - {msg}"


talkers = {
    "GA": "Galileo",
    "GB": "BeiDou",
    "GI": "NavIC",
    "GL": "GLONASS",
    "GP": "GPS",
    "GQ": "QZSS",
    "GN": "GNSS",
}

# Main loop runs forever printing the location, etc. every second.
last_print = time.monotonic()
while True:
    # Make sure to call gps.update() every loop iteration and at least twice
    # as fast as data comes from the GPS unit (usually every second).
    # This returns a bool that's true if it parsed new data (you can ignore it
    # though if you don't care and instead look at the has_fix property).
    if not gps.update() or not gps.has_fix:
        time.sleep(0.1)
        continue

    if gps.nmea_sentence[3:6] == "GSA":
        print(f"{gps.latitude:.6f}, {gps.longitude:.6f} {gps.altitude_m}m")
        print(f"2D Fix: {gps.has_fix}  3D Fix: {gps.has_3d_fix}")
        print(f"  PDOP (Position Dilution of Precision): {format_dop(gps.pdop)}")
        print(f"  HDOP (Horizontal Dilution of Precision): {format_dop(gps.hdop)}")
        print(f"  VDOP (Vertical Dilution of Precision): {format_dop(gps.vdop)}")
        print("Satellites used for fix:")
        for s in gps.sat_prns:
            talker = talkers[s[0:2]]
            number = s[2:]
            print(f"  {talker}-{number} ", end="")
            if gps.sats is None:
                print("- no info")
            else:
                try:
                    sat = gps.sats[s]
                    if sat is None:
                        print("- no info")
                    else:
                        print(f"Elevation:{sat[1]}* Azimuth:{sat[2]}* SNR:{sat[3]}dB")
                except KeyError:
                    print("- no info")
        print()
