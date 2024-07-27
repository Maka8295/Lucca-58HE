# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time

import board
import busio
import digitalio

from adafruit_tinylora.adafruit_tinylora import TTN, TinyLoRa

try:  # typing
    from typing import Annotated, TypeAlias

    bytearray4: TypeAlias = Annotated[bytearray, 4]
    bytearray16: TypeAlias = Annotated[bytearray, 16]
except ImportError:
    pass

# Board LED
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# RFM9x Breakout Pinouts
cs = digitalio.DigitalInOut(board.D5)
irq = digitalio.DigitalInOut(board.D6)
rst = digitalio.DigitalInOut(board.D4)

# Feather M0 RFM9x Pinouts
# cs = digitalio.DigitalInOut(board.RFM9X_CS)
# irq = digitalio.DigitalInOut(board.RFM9X_D0)
# rst = digitalio.DigitalInOut(board.RFM9X_RST)

# TTN Device Address, 4 Bytes, MSB
devaddr: bytearray4 = bytearray([0x00, 0x00, 0x00, 0x00])

# TTN Network Key, 16 Bytes, MSB
nwkey: bytearray16 = bytearray(
    [
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
    ]
)

# TTN Application Key, 16 Bytess, MSB
app: bytearray16 = bytearray(
    [
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
    ]
)

ttn_config = TTN(devaddr, nwkey, app, country="US")

lora = TinyLoRa(spi, cs, irq, rst, ttn_config)

while True:
    data: bytearray4 = bytearray(b"\x43\x57\x54\x46")
    print("Sending packet...")
    lora.send_data(data, len(data), lora.frame_counter)
    print("Packet sent!")
    led.value = True
    lora.frame_counter += 1
    time.sleep(1)
    led.value = False
