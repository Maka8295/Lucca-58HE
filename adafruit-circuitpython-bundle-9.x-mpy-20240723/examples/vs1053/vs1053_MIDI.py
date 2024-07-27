# SPDX-FileCopyrightText: 2021 Eric Rosenbaum
# SPDX-License-Identifier: MIT

import time
import board
import busio

VS1053_BANK_DEFAULT = 0x00
VS1053_BANK_DRUMS1 = 0x78
VS1053_BANK_DRUMS2 = 0x7F
VS1053_BANK_MELODY = 0x79
MIDI_NOTE_ON = 0x90
MIDI_NOTE_OFF = 0x80
MIDI_CHAN_MSG = 0xB0
MIDI_CHAN_BANK = 0x00
MIDI_CHAN_VOLUME = 0x07
MIDI_CHAN_PAN = 0x0A
MIDI_CHAN_PROGRAM = 0xC0

uart = busio.UART(board.TX, board.RX, baudrate=31250)


def note_on(channel, note, vel):
    uart.write(bytearray([MIDI_NOTE_ON | channel, note, vel]))


def note_off(channel, note):
    uart.write(bytearray([MIDI_NOTE_OFF | channel, note, 0]))


def set_channel_bank(channel, bank):
    uart.write(bytearray([MIDI_CHAN_MSG | channel, MIDI_CHAN_BANK, bank]))


def set_channel_volume(channel, vol):
    uart.write(bytearray([MIDI_CHAN_MSG | channel, MIDI_CHAN_VOLUME, vol]))


def set_channel_instrument(channel, num):
    uart.write(bytearray([MIDI_CHAN_PROGRAM | channel]))
    time.sleep(0.01)
    uart.write(bytearray([num]))
    time.sleep(0.01)


def set_channel_pan(channel, pan):
    uart.write(bytearray([MIDI_CHAN_MSG | channel, MIDI_CHAN_PAN, pan]))


# Set up a piano instrument on channel 0
set_channel_bank(0, VS1053_BANK_MELODY)
set_channel_volume(0, 127)
set_channel_instrument(0, 0)  # piano

# Play Do Re Mi
note_on(0, 60, 127)
time.sleep(0.5)
note_off(0, 60)

note_on(0, 62, 127)
time.sleep(0.5)
note_off(0, 62)

note_on(0, 64, 127)
time.sleep(0.5)
note_off(0, 64)

time.sleep(1)

# Play a major scale on all 127 instruments!
# See the datasheet page 32 for a list of instruments:
# https://cdn-shop.adafruit.com/datasheets/vs1053.pdf
scale = [60, 62, 64, 65, 67, 69, 71, 72]
for instrument in range(127):
    print("instrument: " + str(instrument))
    set_channel_instrument(0, instrument)
    for note_num in scale:
        note_on(0, note_num, 127)
        time.sleep(0.1)
    time.sleep(1)
    for note_num in scale:
        note_off(0, note_num)
    time.sleep(0.5)
