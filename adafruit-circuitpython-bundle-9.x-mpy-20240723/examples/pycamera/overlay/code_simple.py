# SPDX-FileCopyrightText: Copyright (c) 2023 john park for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2024 Tim Cocks for Adafruit Industries
#
# SPDX-License-Identifier: MIT
""" simple point-and-shoot camera example, with an overlay frame image. """

import time
import traceback
import adafruit_pycamera  # pylint: disable=import-error

pycam = adafruit_pycamera.PyCamera()
pycam.mode = 0  # only mode 0 (JPEG) will work in this example

# User settings - try changing these:
pycam.resolution = 1  # 0-12 preset resolutions:
#                      0: 240x240, 1: 320x240, 2: 640x480

pycam.led_level = 1  # 0-4 preset brightness levels
pycam.led_color = 0  # 0-7  preset colors: 0: white, 1: green, 2: yellow, 3: red,
#                                          4: pink, 5: blue, 6: teal, 7: rainbow
pycam.effect = 0  # 0-7 preset FX: 0: normal, 1: invert, 2: b&w, 3: red,
#                                  4: green, 5: blue, 6: sepia, 7: solarize

print("Overlay example camera ready.")
pycam.tone(800, 0.1)
pycam.tone(1200, 0.05)

pycam.overlay = "/heart_frame_rgb888.bmp"
pycam.overlay_transparency_color = 0xE007

while True:
    pycam.blit(pycam.continuous_capture())
    pycam.keys_debounce()

    if pycam.shutter.short_count:
        print("Shutter released")
        pycam.tone(1200, 0.05)
        pycam.tone(1600, 0.05)
        try:
            pycam.display_message("snap", color=0x00DD00)
            pycam.capture_jpeg()
            pycam.display_message("overlay", color=0x00DD00)
            pycam.blit_overlay_into_last_capture()
            pycam.live_preview_mode()
        except TypeError as exception:
            traceback.print_exception(exception)
            pycam.display_message("Failed", color=0xFF0000)
            time.sleep(0.5)
            pycam.live_preview_mode()
        except RuntimeError as exception:
            pycam.display_message("Error\nNo SD Card", color=0xFF0000)
            time.sleep(0.5)

    if pycam.card_detect.fell:
        print("SD card removed")
        pycam.unmount_sd_card()
        pycam.display.refresh()

    if pycam.card_detect.rose:
        print("SD card inserted")
        pycam.display_message("Mounting\nSD Card", color=0xFFFFFF)
        for _ in range(3):
            try:
                print("Mounting card")
                pycam.mount_sd_card()
                print("Success!")
                break
            except OSError as exception:
                print("Retrying!", exception)
                time.sleep(0.5)
        else:
            pycam.display_message("SD Card\nFailed!", color=0xFF0000)
            time.sleep(0.5)
        pycam.display.refresh()
