# SPDX-FileCopyrightText: 2024 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""Image viewer

This will display all *jpeg* format images on the inserted SD card.

Press up or down to move by +- 10 images.
Press left or right to move by +- 1 image.

Otherwise, images cycle every DISPLAY_INTERVAL milliseconds (default 8000 = 8 seconds)
"""

import time
import os
import displayio
from jpegio import JpegDecoder
from adafruit_ticks import ticks_less, ticks_ms, ticks_add, ticks_diff
from adafruit_pycamera import PyCameraBase

DISPLAY_INTERVAL = 8000  # milliseconds

decoder = JpegDecoder()

pycam = PyCameraBase()
pycam.init_display()


def load_resized_image(bitmap, filename):
    print(f"loading {filename}")
    bitmap.fill(0b01000_010000_01000)  # fill with a middle grey

    bw, bh = bitmap.width, bitmap.height
    t0 = ticks_ms()
    h, w = decoder.open(filename)
    t1 = ticks_ms()
    print(f"{ticks_diff(t1, t0)}ms to open")
    scale = 0
    print(f"Full image size is {w}x{h}")
    print(f"Bitmap is {bw}x{bh} pixels")
    while (w >> scale) > bw or (h >> scale) > bh and scale < 3:
        scale += 1
    sw = w >> scale
    sh = h >> scale
    print(f"will load at {scale=}, giving {sw}x{sh} pixels")

    if sw > bw:  # left/right sides cut off
        x = 0
        x1 = (sw - bw) // 2
    else:  # horizontally centered
        x = (bw - sw) // 2
        x1 = 0

    if sh > bh:  # top/bottom sides cut off
        y = 0
        y1 = (sh - bh) // 2
    else:  # vertically centered
        y = (bh - sh) // 2
        y1 = 0

    print(f"{x=} {y=} {x1=} {y1=}")
    decoder.decode(bitmap, x=x, y=y, x1=x1, y1=y1, scale=scale)
    t1 = ticks_ms()
    print(f"{ticks_diff(t1, t0)}ms to decode")


def mount_sd():
    if not pycam.card_detect.value:
        pycam.display_message("No SD card\ninserted", color=0xFF0000)
        return []
    pycam.display_message("Mounting\nSD Card", color=0xFFFFFF)
    for _ in range(3):
        try:
            print("Mounting card")
            pycam.mount_sd_card()
            print("Success!")
            break
        except OSError as e:
            print("Retrying!", e)
            time.sleep(0.5)
    else:
        pycam.display_message("SD Card\nFailed!", color=0xFF0000)
        time.sleep(0.5)
    all_images = [
        f"/sd/{filename}"
        for filename in os.listdir("/sd")
        if filename.lower().endswith(".jpg")
    ]
    pycam.display_message(f"Found {len(all_images)}\nimages", color=0xFFFFFF)
    time.sleep(0.5)
    pycam.display.refresh()
    return all_images


def main():
    image_counter = 0
    last_image_counter = 0
    deadline = ticks_ms()
    all_images = mount_sd()

    bitmap = displayio.Bitmap(pycam.display.width, pycam.display.height, 65535)

    while True:
        pycam.keys_debounce()
        if pycam.card_detect.fell:
            print("SD card removed")
            pycam.unmount_sd_card()
            pycam.display_message("SD Card\nRemoved", color=0xFFFFFF)
            time.sleep(0.5)
            pycam.display.refresh()
            all_images = []

        now = ticks_ms()
        if pycam.card_detect.rose:
            print("SD card inserted")
            all_images = mount_sd()
            image_counter = 0
            deadline = now

        if all_images:
            if pycam.up.fell:
                image_counter = (last_image_counter - 10) % len(all_images)
                deadline = now

            if pycam.down.fell:
                image_counter = (last_image_counter + 10) % len(all_images)
                deadline = now

            if pycam.left.fell:
                image_counter = (last_image_counter - 1) % len(all_images)
                deadline = now

            if pycam.right.fell:
                image_counter = (last_image_counter + 1) % len(all_images)
                deadline = now

            if ticks_less(deadline, now):
                print(now, deadline, ticks_less(deadline, now), all_images)
                deadline = ticks_add(deadline, DISPLAY_INTERVAL)
                filename = all_images[image_counter]
                last_image_counter = image_counter
                image_counter = (image_counter + 1) % len(all_images)
                try:
                    load_resized_image(bitmap, filename)
                except Exception as e:  # pylint: disable=broad-exception-caught
                    pycam.display_message(f"Failed to read\n{filename}", color=0xFF0000)
                    print(e)
                    deadline = ticks_add(now, 500)
                pycam.blit(bitmap, y_offset=0)


main()
