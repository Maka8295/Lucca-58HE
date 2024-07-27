# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# The MIT License (MIT)
#
# Copyright (c) 2018 Shawn Hymel for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`BoardTest Suite`
====================================================
CircuitPython board hardware test suite

* Author(s): Shawn Hymel
* Date: December 8, 2018

Implementation Notes
--------------------
Run this to test various input/output abilities of a board. Tests the
following:

* Onboard LEDs
* GPIO output
* Onboard battery voltage monitor
* SPI
* I2C

You will need the following components:

* Multimeter
* LED
* 1x 330 Ohm resistor or 220 Ohm resistor
* 2x 4.7k Ohm resistor
* Microchip 25AA040A SPI EEPROM
* Microchip AT24HC04B I2C EEPROM
* Breadboard
* Wires

Copy the following files to the adafruit_boardtest folder on your CIRCUITPY drive:

* __init__.py
* boardtest_gpio.mpy
* boardtest_i2c.mpy
* boardtest_led.mpy
* boardtest_spi.mpy
* boardtest_uart.mpy
* boardtest_voltage_monitor

Copy this file to the root directory of your CIRCUITPY drive and rename the
filename to code.py. Open a serial terminal, and follow the prompts to run
the various tests.
"""

import board

from adafruit_boardtest import boardtest_led
from adafruit_boardtest import boardtest_gpio
from adafruit_boardtest import boardtest_voltage_monitor
from adafruit_boardtest import boardtest_uart
from adafruit_boardtest import boardtest_spi
from adafruit_boardtest import boardtest_i2c

# Constants
UART_TX_PIN_NAME = "TX"
UART_RX_PIN_NAME = "RX"
UART_BAUD_RATE = 9600
SPI_MOSI_PIN_NAME = "MOSI"
SPI_MISO_PIN_NAME = "MISO"
SPI_SCK_PIN_NAME = "SCK"
SPI_CS_PIN_NAME = "D2"
I2C_SDA_PIN_NAME = "SDA"
I2C_SCL_PIN_NAME = "SCL"

# Results dictionary
TEST_RESULTS = {}

# Save tested pins
PINS_TESTED = []

# Print welcome message
print()
print("                            ....                                      ")
print("                        #@@%%%%%%&@@/                                 ")
print("                     (&@%%%%%%%%%%%%%@&                               ")
print("                  .(@&%%%@*    *&%%%%%%@.                             ")
print("            ,@@&&%%%%%%%%//@%,/ /&%%%%%%@                             ")
print("            %@%%%&%%%%%%%#(@@@&&%%%%%%%%@*                            ")
print("             @&%%&%%%%%%%%%%%%%%%%%%%%%%@/                            ")
print("               &@@&%%%%&&&%%%%%%%%%%%%%%@,                            ")
print("                ,/ &@&&%%%%%%%%%%%%%%%%%@                             ")
print("               ,*        *@&%%%%%%%%%%%%#                             ")
print("               (           @%%%%%%%%%%%@                              ")
print("              ,            @%%%%%%%%%%&@                              ")
print("                          #&%%%%%%%%%%@.                              ")
print("                         #@###%%%%%%%@/                               ")
print("                        (@##(%%%%%%%@%                                ")
print("                       /@###(#%%%%%&@                                 ")
print("                      #@####%%%%%%%@                                  ")
print("                     (@###(%%%%%%%@,                                  ")
print("                    .@##(((#%%%%%&(         .,,.                      ")
print("                   ,@#####%%%%%%%@    ,%@@%%%%%%%&@%                  ")
print("                ,#&@####(%%%%%%%@@@@@&%%%%%%%%%%%###&                 ")
print("               @%%@%####(#%%%%%&@%%%%%%%%%%%%%%##/((@@@@&*            ")
print("              (##@%#####%%%%%%%@(#%%%(/####(/####(%@%%%%%%@/          ")
print("           (@&%@@###(#%%%%%%@&/####(/#####/#&@@&%%%%%%%##@            ")
print("          #@%%%%@#####(#%%%%%%@@@@@@@@@@@@@&%%%%%%%%%%%%#/(@@@@@/     ")
print("          @%(/#@%######%%%%%%%@%%%%%%%%%%%%%%%%%%%%%(/(###@%%%%%%@%   ")
print("         .@@#(#@#####(#%%%%%%&@###//#####/#####/(####/#%@&%%%%%%%%&&  ")
print("        /@%%&@@@(#((((#%%%%%%&@###((#####/#####((##%@@&%%%%%%%%%%%/@. ")
print("       ,@%%%%%%#####%%%%%%%%@@@@&&&&&&&%&@@@@@@&%%%%%%%%%%%%%%%##@,   ")
print("       %%%%%%%%@######(%%%%%%%@&%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#/(#&&  ")
print("       (@###/(%@##((##(%%%%%%%%@%%%%%%%%%%%%%%%%%%%%%%%%%##%###/(&&   ")
print("    ,@@%@%##((#%@#######%%%%%%%%@&%%%%##%%%%##%%%%#/#####((####(@*    ")
print("  *&(,    %@@%##%@#######(%%%%%%%%@#/#####((#####(#####(/#&@&.        ")
print("                 .@###((#%%%%%%%%%&@@###((#####(###%@@&,              ")
print("                   #@#(#######%&@@&* .*#&@@@@@@@%(,                   ")
print("                          .,,,..                                      ")
print()
print("**********************************************************************")
print("*           Welcome to the CircuitPython board test suite!           *")
print("*              Follow the directions to run each test.               *")
print("**********************************************************************")
print()

# List out all the pins available to us
PINS = list(dir(board))
print("All pins found:", end=" ")

# Print pins
for pin in PINS:
    print(pin, end=" ")
print("\n")

# Run LED test
print("@)}---^-----  LED TEST  -----^---{(@")
print()
RESULT = boardtest_led.run_test(PINS)
TEST_RESULTS["LED Test"] = RESULT[0]
PINS_TESTED.append(RESULT[1])
print()
print(RESULT[0])
print()

# Run GPIO test
print("@)}---^-----  GPIO TEST  -----^---{(@")
print()
RESULT = boardtest_gpio.run_test(PINS)
TEST_RESULTS["GPIO Test"] = RESULT[0]
PINS_TESTED.append(RESULT[1])
print()
print(RESULT[0])
print()

# Run voltage monitor test
print("@)}---^-----  VOLTAGE MONITOR TEST  -----^---{(@")
print()
RESULT = boardtest_voltage_monitor.run_test(PINS)
TEST_RESULTS["Voltage Monitor Test"] = RESULT[0]
PINS_TESTED.append(RESULT[1])
print()
print(RESULT[0])
print()

# Run UART test
print("@)}---^-----  UART TEST  -----^---{(@")
print()
RESULT = boardtest_uart.run_test(
    PINS, UART_TX_PIN_NAME, UART_RX_PIN_NAME, UART_BAUD_RATE
)
TEST_RESULTS["UART Test"] = RESULT[0]
PINS_TESTED.append(RESULT[1])
print()
print(RESULT[0])
print()

# Run SPI test
print("@)}---^-----  SPI TEST  -----^---{(@")
print()
RESULT = boardtest_spi.run_test(
    PINS,
    mosi_pin=SPI_MOSI_PIN_NAME,
    miso_pin=SPI_MISO_PIN_NAME,
    sck_pin=SPI_SCK_PIN_NAME,
    cs_pin=SPI_CS_PIN_NAME,
)
TEST_RESULTS["SPI Test"] = RESULT[0]
PINS_TESTED.append(RESULT[1])
print()
print(RESULT[0])
print()

# Run I2C test
print("@)}---^-----  I2C TEST  -----^---{(@")
print()
RESULT = boardtest_i2c.run_test(
    PINS, sda_pin=I2C_SDA_PIN_NAME, scl_pin=I2C_SCL_PIN_NAME
)
TEST_RESULTS["I2C Test"] = RESULT[0]
PINS_TESTED.append(RESULT[1])
print()
print(RESULT[0])
print()

# Print out test results
print("@)}---^-----  TEST RESULTS  -----^---{(@")
print()

# Find appropriate spaces for printing test results
NUM_SPACES = 0
for key in TEST_RESULTS:
    if len(key) > NUM_SPACES:
        NUM_SPACES = len(key)

# Print test results
for key, val in TEST_RESULTS.items():
    print(key + ":", end=" ")
    for i in range(NUM_SPACES - len(key)):
        print(end=" ")
    print(val)
print()

# Figure out which pins were tested and not tested
TESTED = []
for sublist in PINS_TESTED:
    for pin in sublist:
        TESTED.append(pin)
NOT_TESTED = list(set(PINS).difference(set(TESTED)))

# Print tested pins
print("The following pins were tested:", end=" ")
for pin in TESTED:
    print(pin, end=" ")
print("\n")

# Print pins not tested
print("The following pins were NOT tested:", end=" ")
for pin in NOT_TESTED:
    print(pin, end=" ")
print("\n")
