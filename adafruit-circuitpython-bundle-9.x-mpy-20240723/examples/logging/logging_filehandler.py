# SPDX-FileCopyrightText: 2021 Alec Delaney
# SPDX-License-Identifier: MIT

import board
import busio
from digitalio import DigitalInOut
import storage
import adafruit_sdcard
import adafruit_logging as logging
from adafruit_logging import FileHandler

# Get chip select pin depending on the board, this one is for the Feather M4 Express
sd_cs = board.D10

# Set up an SD card to write to
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs = DigitalInOut(sd_cs)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# Initialize log functionality
log_filepath = "/sd/testlog.log"
logger = logging.getLogger("testlog")
file_handler = FileHandler(log_filepath)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

logger.info("Logger initialized!")
logger.debug("You can even add debug statements to the log!")

# If you're done with the FileHandler, close it
file_handler.close()
