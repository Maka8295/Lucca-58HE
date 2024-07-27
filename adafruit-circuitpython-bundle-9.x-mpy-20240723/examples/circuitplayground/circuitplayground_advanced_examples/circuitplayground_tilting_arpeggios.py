# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Tilting Arpeggios

This program plays notes from arpeggios in a circle of fourths. Y-axis tilt chooses the note.
Buttons A and B advance forward and backward through the circle. The switch selects
the type of arpeggio, either dominant seventh or blues.

You can ignore the FrequencyProvider class if you’re just interested in the Circuit Playground
interface.

See a code walkthrough here: https://www.youtube.com/watch?v=cDhqyT3ZN0g
"""

# pylint: disable=R0903
import time
from adafruit_circuitplayground import cp

HS_OCT = 12  # Half-steps per octave
HS_4TH = 5  # Half-steps in a fourth
ARPEGGIOS = ((0, 4, 7, 10), (0, 3, 5, 6, 7, 10))  # Dominant seventh  # Blues
NUM_OCTAVES = 2
STARTING_NOTE = 233.08
MIN_NOTE_PLAY_SECONDS = 0.25
BUTTON_REPEAT_AFTER_SECONDS = 0.25


class FrequencyMaker:
    """Provide frequencies for playing notes"""

    def __init__(self):
        num_octaves_to_pre_compute = NUM_OCTAVES + 2
        num_freqs = HS_OCT * num_octaves_to_pre_compute

        def calc_freq(i):
            return STARTING_NOTE * 2 ** (i / HS_OCT)

        self.note_frequencies = [calc_freq(i) for i in range(num_freqs)]
        self.arpeg_note_indexes = FrequencyMaker.create_arpeggios(
            num_octaves_to_pre_compute
        )
        self.circle_pos = 0
        self.key_offset = 0

    @staticmethod
    def create_arpeggios(num_octaves):
        """Create a list of arpeggios, where each one is a list of chromatic scale note indexes"""
        return [
            FrequencyMaker.create_arpeggio(arpeggio, num_octaves)
            for arpeggio in ARPEGGIOS
        ]

    @staticmethod
    def create_arpeggio(arpeggio, num_octaves):
        return [
            octave * HS_OCT + note for octave in range(num_octaves) for note in arpeggio
        ]

    def advance(self, amount):
        """Advance forward or backward through the circle of fourths"""
        self.circle_pos = (self.circle_pos + amount) % HS_OCT
        self.key_offset = self.circle_pos * HS_4TH % HS_OCT

    def freq(self, normalized_position, selected_arpeg):
        """Return the frequency for the note at the specified position in the specified arpeggio"""
        selected_arpeg_note_indexes = self.arpeg_note_indexes[selected_arpeg]
        num_notes_in_selected_arpeg = len(ARPEGGIOS[selected_arpeg])
        num_arpeg_notes_in_range = num_notes_in_selected_arpeg * NUM_OCTAVES + 1
        arpeg_index = int(normalized_position * num_arpeg_notes_in_range)
        note_index = self.key_offset + selected_arpeg_note_indexes[arpeg_index]
        return self.note_frequencies[note_index]


class ButtonDetector:
    def __init__(self):
        self.next_press_allowed_at = time.monotonic()
        self.buttons_on = (cp.button_a, cp.button_b)

    def pressed(self, index):
        """Return whether the specified button (0=A, 1=B) was pressed, limiting the repeat rate"""
        pressed = cp.button_b if index else cp.button_a
        if pressed:
            now = time.monotonic()
            if now >= self.next_press_allowed_at:
                self.next_press_allowed_at = now + BUTTON_REPEAT_AFTER_SECONDS
                return True
        return False


class TiltingArpeggios:
    def __init__(self):
        cp.pixels.brightness = 0.2
        self.freq_maker = FrequencyMaker()
        TiltingArpeggios.update_pixel(self.freq_maker.circle_pos)
        self.button = ButtonDetector()
        self.last_freq = None
        self.next_freq_change_allowed_at = time.monotonic()

    def run(self):
        while True:
            self.process_button_presses()
            if time.monotonic() >= self.next_freq_change_allowed_at:
                self.next_freq_change_allowed_at = (
                    time.monotonic() + MIN_NOTE_PLAY_SECONDS
                )
                self.change_tone_if_needed()

    @staticmethod
    def update_pixel(circle_pos):
        """Manage the display on the NeoPixels of the current circle position"""
        cp.pixels.fill((0, 0, 0))
        # Light the pixels clockwise from “1 o’clock” with the USB connector on the bottom
        pixel_index = (4 - circle_pos) % 10
        # Use a different color after all ten LEDs used
        color = (0, 255, 0) if circle_pos <= 9 else (255, 255, 0)
        cp.pixels[pixel_index] = color

    @staticmethod
    def tilt():
        """Normalize the Y-Axis Tilt"""
        standard_gravity = (
            9.81  # Acceleration (m/s²) due to gravity at the earth’s surface
        )
        constrained_accel = min(max(0.0, -cp.acceleration[1]), standard_gravity)
        return constrained_accel / standard_gravity

    def process_button_presses(self):
        """For each of the buttons A and B, if pushed, advance forward or backward"""
        for button_index, direction in enumerate((1, -1)):
            if self.button.pressed(button_index):
                self.freq_maker.advance(direction)
                TiltingArpeggios.update_pixel(self.freq_maker.circle_pos)

    def change_tone_if_needed(self):
        """Find the frequency for the current arpeggio and tilt, and restart the tone if changed"""
        arpeggio_index = 0 if cp.switch else 1
        freq = self.freq_maker.freq(TiltingArpeggios.tilt(), arpeggio_index)
        if freq != self.last_freq:
            self.last_freq = freq
            cp.stop_tone()
            cp.start_tone(freq)


TiltingArpeggios().run()
