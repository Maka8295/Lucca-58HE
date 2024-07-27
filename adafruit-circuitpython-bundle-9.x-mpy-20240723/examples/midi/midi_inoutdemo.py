# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# midi_inoutdemo - demonstrates receiving and sending MIDI events

import usb_midi

import adafruit_midi

# pylint: disable=unused-import
from adafruit_midi.channel_pressure import ChannelPressure
from adafruit_midi.control_change import ControlChange
from adafruit_midi.midi_message import MIDIUnknownEvent
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.pitch_bend import PitchBend
from adafruit_midi.polyphonic_key_pressure import PolyphonicKeyPressure
from adafruit_midi.program_change import ProgramChange
from adafruit_midi.start import Start
from adafruit_midi.stop import Stop
from adafruit_midi.system_exclusive import SystemExclusive
from adafruit_midi.timing_clock import TimingClock

# TimingClock is worth importing first if present as it
# will make parsing more efficient for this high frequency event
# Only importing what is used will save a little bit of memory


midi = adafruit_midi.MIDI(
    midi_in=usb_midi.ports[0],
    midi_out=usb_midi.ports[1],
    in_channel=(1, 2, 3),
    out_channel=0,
)

print("Midi Demo in and out")

# Convert channel numbers at the presentation layer to the ones musicians use
print("Default output channel:", midi.out_channel + 1)
print("Listening on input channels:", tuple(c + 1 for c in midi.in_channel))

major_chord = [0, 4, 7]
while True:
    while True:
        msg_in = midi.receive()  # non-blocking read
        # For a Note On or Note Off play a major chord
        # For any other known event just forward it
        if isinstance(msg_in, NoteOn) and msg_in.velocity != 0:
            print(
                "Playing major chord with root",
                msg_in.note,
                "from channel",
                msg_in.channel + 1,
            )
            for offset in major_chord:
                new_note = msg_in.note + offset
                if 0 <= new_note <= 127:
                    midi.send(NoteOn(new_note, msg_in.velocity))

        elif (
            isinstance(msg_in, NoteOff)
            or isinstance(msg_in, NoteOn)
            and msg_in.velocity == 0
        ):
            for offset in major_chord:
                new_note = msg_in.note + offset
                if 0 <= new_note <= 127:
                    midi.send(NoteOff(new_note, 0x00))

        elif isinstance(msg_in, MIDIUnknownEvent):
            # Message are only known if they are imported
            print("Unknown MIDI event status ", msg_in.status)

        elif msg_in is not None:
            midi.send(msg_in)
