# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Check memory usage

# pylint: disable=multiple-statements,unused-import,wrong-import-position,no-member

# The disable for no-member should not really be required
# probably a difference between Python 3 module and micropython
#
# E:  8,21: Module 'gc' has no 'mem_free' member (no-member)

import gc
import random
import time

gc.collect()
print(gc.mem_free())
import usb_midi

gc.collect()
print(gc.mem_free())
import adafruit_midi

gc.collect()
print(gc.mem_free())

# Full monty
from adafruit_midi.channel_pressure import ChannelPressure

gc.collect()
print(gc.mem_free())
from adafruit_midi.control_change import ControlChange

gc.collect()
print(gc.mem_free())
from adafruit_midi.note_off import NoteOff

gc.collect()
print(gc.mem_free())
from adafruit_midi.note_on import NoteOn

gc.collect()
print(gc.mem_free())
from adafruit_midi.pitch_bend import PitchBend

gc.collect()
print(gc.mem_free())
from adafruit_midi.polyphonic_key_pressure import PolyphonicKeyPressure

gc.collect()
print(gc.mem_free())
from adafruit_midi.program_change import ProgramChange

gc.collect()
print(gc.mem_free())
from adafruit_midi.start import Start

gc.collect()
print(gc.mem_free())
from adafruit_midi.stop import Stop

gc.collect()
print(gc.mem_free())
from adafruit_midi.system_exclusive import SystemExclusive

gc.collect()
print(gc.mem_free())
from adafruit_midi.timing_clock import TimingClock

gc.collect()
print(gc.mem_free())

midi = adafruit_midi.MIDI(
    midi_in=usb_midi.ports[0], midi_out=usb_midi.ports[1], in_channel=0, out_channel=0
)

gc.collect()
print(gc.mem_free())
