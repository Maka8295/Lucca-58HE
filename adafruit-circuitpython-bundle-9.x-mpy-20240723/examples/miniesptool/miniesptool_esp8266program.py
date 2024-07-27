# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
from digitalio import DigitalInOut
import adafruit_miniesptool

print("ESP8266 mini prog")

uart = busio.UART(board.TX, board.RX, baudrate=115200, timeout=1)
resetpin = DigitalInOut(board.D5)
gpio0pin = DigitalInOut(board.D6)
# On ESP8266 we will 'sync' to the baudrate in initialization
esptool = adafruit_miniesptool.miniesptool(
    uart, gpio0pin, resetpin, flashsize=1024 * 1024, baudrate=256000
)

esptool.debug = False
esptool.sync()

print("Synced")
print(esptool.chip_name)
print("MAC ADDR: ", [hex(i) for i in esptool.mac_addr])
esptool.flash_file("esp8266/AT_firmware_1.6.2.0.bin", 0x0)
# 0x3FC000 esp_init_data_default_v05.bin
esptool.flash_file("esp8266/esp_init_data_default_v05.bin", 0x3FC000)
# 0x3FE000 blank.bin
esptool.flash_file("esp8266/blank.bin", 0x3FE000)
esptool.reset()
time.sleep(0.5)
