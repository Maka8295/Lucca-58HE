# SPDX-FileCopyrightText: 2023 Tim Cocks
#
# SPDX-License-Identifier: MIT

"""Volume Animation Example"""
import board
from audiomp3 import MP3Decoder
import neopixel
from adafruit_led_animation.animation import volume

try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!

# Fill in your own MP3 file or use the one from the learn guide:
# https://learn.adafruit.com/circuitpython-essentials/circuitpython-mp3-audio#installing-project-code-3067700
mp3file = "happy.mp3"
with open(mp3file, "rb") as mp3:
    decoder = MP3Decoder(mp3)
    audio = AudioOut(board.SPEAKER)

    strip_pixels = neopixel.NeoPixel(board.D4, 30, brightness=0.1, auto_write=False)
    volume_anim = volume.Volume(strip_pixels, 0.3, (0, 255, 0), decoder, 400)

    while True:
        audio.play(decoder)
        print("playing", mp3file)

        while audio.playing:
            volume_anim.animate()
