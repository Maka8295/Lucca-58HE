# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Arduino Mega 2560 programming example, be sure you have the Mega/2560 wired up so:
  Mega Ground to CircuitPython GND
  Mega 5V to CircuitPython USB or make sure the Trinket is powered by USB
  Pin 52 -> CircuitPython SCK
  Pin 50 -> CircuitPython MISO  - Note this is backwards from what you expect
  Pin 51 -> CircuitPython MOSI  - Note this is backwards from what you expect
  RESET  -> CircuitPython D5 (or change the init() below to change it)
Drag "stk500boot_v2_mega2560.hex" onto the CircuitPython disk drive, then open REPL
"""

import board
import busio
import adafruit_avrprog

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
avrprog = adafruit_avrprog.AVRprog()
avrprog.init(spi, board.D5)

# To program a chip, you'll need to find out the signature, size of the flash,
# flash-page size and fuse mask. You can find this in the datasheet or in
# avrdude.conf located at:
# http://svn.savannah.nongnu.org/viewvc/*checkout*/avrdude/trunk/avrdude/avrdude.conf.in
# You can also use the predefined values in AVRprog.Boards
atmega2560 = {
    "name": "ATmega2560",
    "sig": [0x1E, 0x98, 0x01],
    "flash_size": 262144,
    "page_size": 256,
    "fuse_mask": (0xFF, 0xFF, 0x07, 0x3F),
}


def error(err):
    """Helper to print out errors for us and then halt"""
    print("ERROR: " + err)
    avrprog.end()
    while True:
        pass


while input("Ready to GO, type 'G' here to start> ") != "G":
    pass

if not avrprog.verify_sig(atmega2560, verbose=True):
    error("Signature read failure")
print("Found", atmega2560["name"])

# Since we are unsetting the lock fuse, an erase is required!
avrprog.erase_chip()

avrprog.write_fuses(atmega2560, low=0xFF, high=0xD8, ext=0x05, lock=0x3F)
if not avrprog.verify_fuses(atmega2560, low=0xFF, high=0xD8, ext=0x05, lock=0x3F):
    error(
        "Failure programming fuses: "
        + str([hex(i) for i in avrprog.read_fuses(atmega2560)])
    )

print("Programming flash from file")
avrprog.program_file(
    atmega2560, "stk500boot_v2_mega2560.hex", verbose=True, verify=True
)

avrprog.write_fuses(atmega2560, lock=0x0F)
if not avrprog.verify_fuses(atmega2560, lock=0x0F):
    error("Failure verifying fuses!")

print("Done!")
