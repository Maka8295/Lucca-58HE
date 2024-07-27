# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
Soundboard example with buttons.
"""

import time
from adafruit_pyportal import PyPortal
from adafruit_button import Button

SHOW_BUTTONS = False

# the current working directory (where this file is)
cwd = ("/" + __file__).rsplit("/", 1)[0]
# No internet use version of pyportal
pyportal = PyPortal(default_bg=cwd + "/button_background.bmp")

spots = []
spots.append({"label": "1", "pos": (10, 10), "size": (60, 60), "file": "01.wav"})
spots.append({"label": "2", "pos": (90, 10), "size": (60, 60), "file": "02.wav"})
spots.append({"label": "3", "pos": (170, 10), "size": (60, 60), "file": "03.wav"})
spots.append({"label": "4", "pos": (250, 10), "size": (60, 60), "file": "04.wav"})
spots.append({"label": "5", "pos": (10, 90), "size": (60, 60), "file": "05.wav"})
spots.append({"label": "6", "pos": (90, 90), "size": (60, 60), "file": "06.wav"})
spots.append({"label": "7", "pos": (170, 90), "size": (60, 60), "file": "07.wav"})
spots.append({"label": "8", "pos": (250, 90), "size": (60, 60), "file": "08.wav"})
spots.append({"label": "9", "pos": (10, 170), "size": (60, 60), "file": "09.wav"})
spots.append({"label": "10", "pos": (90, 170), "size": (60, 60), "file": "10.wav"})
spots.append({"label": "11", "pos": (170, 170), "size": (60, 60), "file": "11.wav"})
spots.append({"label": "12", "pos": (250, 170), "size": (60, 60), "file": "12.wav"})

buttons = []
for spot in spots:
    fill = outline = None
    if SHOW_BUTTONS:
        fill = None
        outline = 0x00FF00
    button = Button(
        x=spot["pos"][0],
        y=spot["pos"][1],
        width=spot["size"][0],
        height=spot["size"][1],
        fill_color=fill,
        outline_color=outline,
        label=spot["label"],
        label_color=None,
        name=spot["file"],
    )
    pyportal.splash.append(button)
    buttons.append(button)

last_pressed = None
currently_pressed = None
while True:
    p = pyportal.touchscreen.touch_point
    if p:
        print(p)
        for b in buttons:
            if b.contains(p):
                print("Touched", b.name)
                if currently_pressed != b:  # don't restart if playing
                    pyportal.play_file(cwd + "/" + b.name, wait_to_finish=False)
                currently_pressed = b
                break
        else:
            currently_pressed = None
    time.sleep(0.05)
