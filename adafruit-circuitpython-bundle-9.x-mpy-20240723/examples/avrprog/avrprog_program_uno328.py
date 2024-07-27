# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
UNO Optiboot programming example, be sure you have the UNO wired up so:
  UNO Ground to CircuitPython GND
  UNO 5V to CircuitPython USB or make sure the UNO is powered by USB
  UNO Pin 13 -> CircuitPython SCK
  UNO Pin 12 -> CircuitPython MISO
  UNO Pin 11 -> CircuitPython MOSI
  UNO RESET  -> CircuitPython D5 (or change the init() below to change it!)
Drag "optiboot_atmega328.hex" onto the CircuitPython disk drive, then open REPL!
"""

import board
import busio
import pwmio
import adafruit_avrprog

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
avrprog = adafruit_avrprog.AVRprog()
avrprog.init(spi, board.D5)

# pylint: disable-msg=no-member
# we can generate an 6 MHz clock for driving bare chips too!
clock_pwm = pwmio.PWMOut(board.D9, frequency=6000000, duty_cycle=65536 // 2)
# pylint: enable-msg=no-member

# Each chip has to have a definition so the script knows how to find it
atmega328p = avrprog.Boards.ATmega328p


def error(err):
    """Helper to print out errors for us and then halt"""
    print("ERROR: " + err)
    avrprog.end()
    while True:
        pass


while input("Ready to GO, type 'G' here to start> ") != "G":
    pass

if not avrprog.verify_sig(atmega328p, verbose=True):
    error("Signature read failure")
print("Found", atmega328p["name"])

# Since we are unsetting the lock fuse, an erase is required!
avrprog.erase_chip()

avrprog.write_fuses(atmega328p, low=0xFF, high=0xDE, ext=0x05, lock=0x3F)
if not avrprog.verify_fuses(atmega328p, low=0xFF, high=0xDE, ext=0x05, lock=0x3F):
    error(
        "Failure programming fuses: "
        + str([hex(i) for i in avrprog.read_fuses(atmega328p)])
    )

print("Programming flash from file")
avrprog.program_file(atmega328p, "optiboot_atmega328.hex", verbose=True, verify=True)

avrprog.write_fuses(atmega328p, lock=0x0F)
if not avrprog.verify_fuses(atmega328p, lock=0x0F):
    error("Failure verifying fuses!")

print("Done!")
