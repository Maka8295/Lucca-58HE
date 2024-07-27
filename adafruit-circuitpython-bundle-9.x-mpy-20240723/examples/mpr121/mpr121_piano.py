# SPDX-FileCopyrightText: 2017 Tony DiCola, Carter Nelson for Adafruit Industries
# SPDX-License-Identifier: MIT

# MPR121 piano demo.
# Listens to the first 7 inputs of the MPR121 and plays a middle scale note
# when an input is touched.  Note only one note is played at a time!
# For use with microcontrollers or computers with PWM support only!


import board
import busio
import pwmio

# Import MPR121 module.
import adafruit_mpr121


# Configure PWM buzzer and other state:
BUZZER_PIN = board.D9
TONE_ON_DUTY = 2**15  # Duty cycle of tone when turned on, a square wave.
TONE_OFF_DUTY = 0  # Duty cycle of tone when turned off, 0 or no signal.
NOTE_FREQS = [
    261,  # Input 0 = 261 hz = middle C
    294,  # Input 1 = middle D
    329,  # Input 2 = middle E
    349,  # Input 3 = middle F
    392,  # Input 4 = middle G
    440,  # Input 5 = middle A
    493,  # Input 6 = middle B
    0,  # Input 7 = nothing (set to a frequency in hertz!)
    0,  # Input 8
    0,  # Input 9
    0,  # Input 10
    0,
]  # Input 11


# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Create MPR121 class.
mpr121 = adafruit_mpr121.MPR121(i2c)
# Note you can optionally change the address of the device:
# mpr121 = adafruit_mpr121.MPR121(i2c, address=0x91)

# pylint: disable-msg=no-member
# Setup buzzer PWM output.
buzzer = pwmio.PWMOut(
    BUZZER_PIN, duty_cycle=TONE_OFF_DUTY, frequency=440, variable_frequency=True
)
# pylint: disable-msg=no-member

last_note = None
while True:
    # Get touched state for all pins
    touched = mpr121.touched_pins
    # If no pins are touched, be quiet
    if True not in touched:
        last_note = None
        buzzer.duty_cycle = TONE_OFF_DUTY
        continue
    # Get index of touched pin
    note = touched.index(True)
    # Play note if pin is different and has a defined note
    if note != last_note and NOTE_FREQS[note] != 0:
        last_note = note
        buzzer.frequency = NOTE_FREQS[note]
        buzzer.duty_cycle = TONE_ON_DUTY
