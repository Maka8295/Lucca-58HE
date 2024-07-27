# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Trinket/Gemma (ATtiny85) programming example, be sure you have the '85 wired up so:
  Trinket Ground to CircuitPython GND
  Trinket USB to CircuitPythong USB or make sure the Trinket is powered by USB
  Pin 2 -> CircuitPython SCK
  Pin 1 -> CircuitPython MISO
  Pin 0 -> CircuitPython MOSI
  RESET  -> CircuitPython D5 (or change the init() below to change it!)
Drag "trinket_boot.hex" onto the CircuitPython disk drive, then open REPL!
"""

import board
import busio
import adafruit_avrprog

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
avrprog = adafruit_avrprog.AVRprog()
avrprog.init(spi, board.D5)

# Each chip has to have a definition so the script knows how to find it
attiny85 = avrprog.Boards.ATtiny85


def error(err):
    """Helper to print out errors for us and then halt"""
    print("ERROR: " + err)
    avrprog.end()
    while True:
        pass


while input("Ready to GO, type 'G' here to start> ") != "G":
    pass

if not avrprog.verify_sig(attiny85, verbose=True):
    error("Signature read failure")
print("Found", attiny85["name"])

avrprog.write_fuses(attiny85, low=0xF1, high=0xD5, ext=0x06, lock=0x3F)
if not avrprog.verify_fuses(attiny85, low=0xF1, high=0xD5, ext=0x06, lock=0x3F):
    error("Failure verifying fuses!")

print("Programming flash from file")
avrprog.program_file(attiny85, "trinket_boot.hex", verbose=True, verify=True)

print("Done!")
