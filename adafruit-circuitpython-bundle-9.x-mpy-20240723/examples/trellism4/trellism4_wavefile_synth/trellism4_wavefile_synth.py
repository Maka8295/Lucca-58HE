# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
This synthesizer is loaded with wave files for 3 octaves of notes each in 4 different waveforms.
It uses Mixer to play up to 7 notes at once.
Play notes with the rainbow buttons. Change waveform types ith the white buttons in the last column.
"""
# pylint: disable=consider-using-with,consider-using-dict-items
import board
from audiocore import WaveFile
from audioio import AudioOut
from audiomixer import Mixer
import adafruit_trellism4

# trellis helper object
trellis = adafruit_trellism4.TrellisM4Express()
# low brightness on the neopixles
trellis.pixels.brightness = 0.05
# each musical note letter
note_letters = ["C", "D", "E", "F", "G", "A", "B"]
# colors of the rainbow
colors = [
    (255, 0, 0),
    (255, 127, 0),
    (255, 255, 0),
    (0, 255, 0),
    (0, 0, 255),
    (56, 43, 105),
    (139, 0, 255),
]

# dictionary holding note string to wave file value.
# e.g. {... "sined4": audioio.WaveFile(open("notes/sine/d4.wav")), ...}
notes = {}

# list of all waveform types
WAVE_TYPES = ["sine", "square", "sawtooth", "triangle"]

# current waveform type. Will get changed from the last column
current_wave_type = "sine"

# load the notes dictionary
for wave_type in WAVE_TYPES:
    for octave in range(3, 6):  # [3,4,5]
        for note_letter in note_letters:
            # note with octave e.g. a4
            cur_note = "{}{}".format(note_letter, octave)
            # add wave file to dictionary
            key = "{}{}".format(wave_type, cur_note)
            notes[key] = WaveFile(
                open("notes/{}/{}.wav".format(wave_type, cur_note), "rb")
            )

# main audio object
audio = AudioOut(left_channel=board.A0, right_channel=board.A1)
# mixer to allow pylyphonic playback
mixer = Mixer(
    voice_count=8,
    sample_rate=8000,
    channel_count=2,
    bits_per_sample=16,
    samples_signed=True,
)

audio.play(mixer)

# turn on the rainbow lights
for i, color in enumerate(colors):
    trellis.pixels[i, 0] = color
    trellis.pixels[i, 1] = color
    trellis.pixels[i, 2] = color

# list of keys pressed on the previous iteration
prev_pressed = []

# voice recycling variables
available_voices = [1, 2, 3, 4, 5, 6, 7]
# key to voice dictionary e.g. {... (1,2):4, (1,3):3,  ...}
used_voices = {}

# waveform selector in the last column
# default to index 0 sine
trellis.pixels[7, 0] = (255, 255, 255)
while True:
    cur_keys = trellis.pressed_keys
    # if the keys are different from previous iteration
    if cur_keys != prev_pressed:
        # loop over currently pressed keys
        for key in cur_keys:
            # if it's a note key. First 7 columns.
            if key[0] < len(note_letters):
                # if we aren't already playing this note and we have available voice
                if key not in used_voices and available_voices:
                    # build not string
                    note_for_key = "{}{}".format(note_letters[key[0]], key[1] + 3)
                    note_to_play = "{}{}".format(current_wave_type, note_for_key)
                    # if the note exists in the notes dictionary
                    if note_to_play in notes:
                        # get an available voice
                        voice_to_use = available_voices.pop()
                        used_voices[key] = voice_to_use
                        # play the note
                        mixer.play(notes[note_to_play], voice=voice_to_use, loop=True)
            else:  # last column
                current_wave_type = WAVE_TYPES[key[1]]
                # turn off all last column pixels
                for y_pixel in range(0, 4):
                    trellis.pixels[7, y_pixel] = (0, 0, 0)
                # turn on selected
                trellis.pixels[7, key[1]] = (255, 255, 255)
        if mixer.playing:
            # loop over each note that is playing
            for key in used_voices:
                # if the key is no longer down
                if key not in cur_keys:
                    # stop playing
                    mixer.stop_voice(used_voices[key])
                    # recycle voice
                    available_voices.append(used_voices[key])
                    used_voices.pop(key, None)
    # update variable for next iteration
    prev_pressed = cur_keys
