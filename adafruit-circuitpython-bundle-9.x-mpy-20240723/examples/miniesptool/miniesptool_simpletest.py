# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
from digitalio import DigitalInOut, Direction  # pylint: disable=unused-import
import adafruit_miniesptool

print("ESP32 Nina-FW")

# Override these if you are manually wiring. Otherwise, this will use ESP pins from board.
tx = getattr(board, "ESP_TX", board.TX)
rx = getattr(board, "ESP_RX", board.RX)
resetpin = getattr(board, "ESP_RESET", board.D12)
gpio0pin = getattr(board, "ESP_GPIO0", board.D10)

uart = busio.UART(tx, rx, baudrate=115200, timeout=1)

esptool = adafruit_miniesptool.miniesptool(
    uart, DigitalInOut(gpio0pin), DigitalInOut(resetpin), flashsize=4 * 1024 * 1024
)
esptool.sync()

print("Synced")
print("Found:", esptool.chip_name)
if esptool.chip_name != "ESP32":
    raise RuntimeError("This example is for ESP32 only")
esptool.baudrate = 912600
print("MAC ADDR: ", [hex(i) for i in esptool.mac_addr])

# Note: Make sure to use the LATEST nina-fw binary release!
esptool.flash_file("NINA_W102-1.7.1.bin", 0x0, "dc81f0433dfba6de33c78b5c5911261d")

esptool.reset()
time.sleep(0.5)
