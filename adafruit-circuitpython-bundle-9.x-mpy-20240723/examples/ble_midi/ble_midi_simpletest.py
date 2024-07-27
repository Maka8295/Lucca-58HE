# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example sends MIDI out. It sends NoteOn and then NoteOff with a random pitch bend.
"""

import time
import random
import adafruit_ble
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
import adafruit_midi
from adafruit_midi.control_change import ControlChange
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.pitch_bend import PitchBend
import adafruit_ble_midi

# Use default HID descriptor
midi_service = adafruit_ble_midi.MIDIService()
advertisement = ProvideServicesAdvertisement(midi_service)
# advertisement.appearance = 961

ble = adafruit_ble.BLERadio()
if ble.connected:
    for c in ble.connections:
        c.disconnect()

midi = adafruit_midi.MIDI(midi_out=midi_service, out_channel=0)

print("advertising")
ble.start_advertising(advertisement)

while True:
    print("Waiting for connection")
    while not ble.connected:
        pass
    print("Connected")
    # Sleep briefly so client can get ready and send setup
    # writes to the MIDIService. 0.5secs was insufficient.
    time.sleep(1.0)
    # Send one unique NoteOn/Off at the beginning to check that the
    # delay is sufficient.
    midi.send(NoteOn(20, 99))
    midi.send(NoteOff(20, 99))
    while ble.connected:
        midi.send(NoteOn(44, 120))  # G sharp 2nd octave
        time.sleep(0.25)
        a_pitch_bend = PitchBend(random.randint(0, 16383))
        midi.send(a_pitch_bend)
        time.sleep(0.25)
        # note how a list of messages can be used
        midi.send([NoteOff("G#2", 120), ControlChange(3, 44)])
        time.sleep(0.5)
    print("Disconnected")
    print()
    ble.start_advertising(advertisement)
