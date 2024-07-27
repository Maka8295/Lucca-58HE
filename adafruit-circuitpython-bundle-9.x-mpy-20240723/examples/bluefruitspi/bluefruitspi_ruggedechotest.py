# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# A more 'rugged' echo test for the Feather M0 Bluefruit
# Sets the name, then echo's all RX'd data with a reversed packet
# we wrap the loop in a try/except block and have multiple loops
# and functions to keep our connection up and running no matter what

import time
import busio
import board
from digitalio import DigitalInOut
from adafruit_bluefruitspi import BluefruitSPI

ADVERT_NAME = b"BlinkaBLE"

spi_bus = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = DigitalInOut(board.D8)
irq = DigitalInOut(board.D7)
rst = DigitalInOut(board.D4)
bluefruit = BluefruitSPI(spi_bus, cs, irq, rst, debug=False)


def init_bluefruit():
    # Initialize the device and perform a factory reset
    print("Initializing the Bluefruit LE SPI Friend module")
    bluefruit.init()
    bluefruit.command_check_OK(b"AT+FACTORYRESET", delay=1)
    # Print the response to 'ATI' (info request) as a string
    print(str(bluefruit.command_check_OK(b"ATI"), "utf-8"))
    # Change advertised name
    bluefruit.command_check_OK(b"AT+GAPDEVNAME=" + ADVERT_NAME)


def wait_for_connection():
    print("Waiting for a connection to Bluefruit LE Connect ...")
    # Wait for a connection ...
    dotcount = 0
    while not bluefruit.connected:
        print(".", end="")
        dotcount = (dotcount + 1) % 80
        if dotcount == 79:
            print("")
        time.sleep(0.5)


# This code will check the connection but only query the module if it has been
# at least 'n_sec' seconds. Otherwise it 'caches' the response, to keep from
# hogging the Bluefruit connection with constant queries
connection_timestamp = None
is_connected = None


def check_connection(n_sec):
    # pylint: disable=global-statement
    global connection_timestamp, is_connected
    if (not connection_timestamp) or (time.monotonic() - connection_timestamp > n_sec):
        connection_timestamp = time.monotonic()
        is_connected = bluefruit.connected
    return is_connected


# Unlike most circuitpython code, this runs in two loops
# one outer loop manages reconnecting bluetooth if we lose connection
# then one inner loop for doing what we want when connected!
while True:
    # Initialize the module
    try:  # Wireless connections can have corrupt data or other runtime failures
        # This try block will reset the module if that happens
        init_bluefruit()
        wait_for_connection()
        print("\n *Connected!*")

        # Once connected, check for incoming BLE UART data
        while check_connection(3):  # Check our connection status every 3 seconds
            # OK we're still connected, see if we have any data waiting
            resp = bluefruit.uart_rx()
            if not resp:
                continue  # nothin'
            print("Read %d bytes: %s" % (len(resp), resp))
            # Now write it!
            print("Writing reverse...")
            send = []
            for i in range(len(resp), 0, -1):
                send.append(resp[i - 1])
            print(bytes(send))
            bluefruit.uart_tx(bytes(send))
        print("Connection lost.")

    except RuntimeError as e:
        print(e)  # Print what happened
        continue  # retry!
