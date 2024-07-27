# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
example of reading temperature and humidity from a DHT device
and displaying results to the serial port and a 8 digit 7-segment display
the DHT device data wire is connected to board.D2
"""
# import for dht devices and 7-segment display devices
import time
from board import D2, TX, RX, D1
import busio
import digitalio
from adafruit_max7219 import bcddigits
import adafruit_dht


clk = RX
din = TX
cs = digitalio.DigitalInOut(D1)
spi = busio.SPI(clk, MOSI=din)
display = bcddigits.BCDDigits(spi, cs, nDigits=8)
display.brightness(5)

# initial the dht device
dhtDevice = adafruit_dht.DHT22(D2)

while True:
    try:
        # show the values to the serial port
        temperature = dhtDevice.temperature * (9 / 5) + 32
        humidity = dhtDevice.humidity
        # print("Temp: {:.1f} F Humidity: {}% ".format(temperature, humidity))

        # now show the values on the 8 digit 7-segment display
        display.clear_all()
        display.show_str(0, "{:5.1f}{:5.1f}".format(temperature, humidity))
        display.show()

    except RuntimeError as error:
        print(error.args[0])

    time.sleep(2.0)
