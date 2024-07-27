# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
ATtiny13a programming example, be sure you have the '13a wired up so:
  ATtiny13a GND to CircuitPython GND
  ATtiny13a VCC to CircuitPython USB
  Pin 2 -> CircuitPython SCK
  Pin 1 -> CircuitPython MISO
  Pin 0 -> CircuitPython MOSI
  RESET  -> CircuitPython D5 (or change the init() below to change it!)
Drag "attiny13a_blink.hex" onto the CircuitPython disk drive, then open REPL!
"""

import board
import busio
import adafruit_avrprog

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
avrprog = adafruit_avrprog.AVRprog()
avrprog.init(spi, board.D5)

# Each chip has to have a definition so the script knows how to find it
attiny13 = avrprog.Boards.ATtiny13a


def error(err):
    """Helper to print out errors for us and then halt"""
    print("ERROR: " + err)
    avrprog.end()
    while True:
        pass


while input("Ready to GO, type 'G' here to start> ") != "G":
    pass

if not avrprog.verify_sig(attiny13, verbose=True):
    error("Signature read failure")
print("Found", attiny13["name"])

avrprog.write_fuses(attiny13, low=0x7A, high=0xFF)
if not avrprog.verify_fuses(attiny13, low=0x7A, high=0xFF):
    error("Failure verifying fuses!")

print("Programming flash from file")
avrprog.program_file(attiny13, "attiny13a_blink.hex", verbose=True, verify=True)

print("Done!")
