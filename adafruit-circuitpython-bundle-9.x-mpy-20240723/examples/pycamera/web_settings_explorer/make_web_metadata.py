# SPDX-FileCopyrightText: 2023 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import json


def list_range(*args):
    return list(range(*args))


metadata = {
    "property": {
        "effect": (
            "Normal",
            "Invert",
            "B&W",
            "Reddish",
            "Greenish",
            "Bluish",
            "Sepia",
            "Solarize",
        ),
        "resolution": (
            "240x240",
            "320x240",
            "640x480",
            "800x600",
            "1024x768",
            "1280x720",
            "1280x1024",
            "1600x1200",
            "1920x1080",
            "2048x1536",
            "2560x1440",
            "2560x1600",
            "2560x1920",
        ),
        "led_level": list_range(5),
        "led_color": list_range(8),
    },
    "property2": {
        # "sensor_name": None,
        "contrast": list_range(-2, 3),
        "brightness": list_range(-2, 3),
        "saturation": list_range(-2, 3),
        "sharpness": list_range(-2, 3),
        "ae_level": list_range(-2, 3),
        "denoise": list_range(10),
        "gain_ceiling": list_range(10),
        "quality": list_range(8, 36),
        "colorbar": [False, True],
        "whitebal": [False, True],
        "gain_ctrl": [False, True],
        "exposure_ctrl": [False, True],
        "hmirror": [False, True],
        "vflip": [False, True],
        "aec2": [False, True],
        "awb_gain": [False, True],
        "dcw": [False, True],
        "bpc": [False, True],
        "wpc": [False, True],
        "raw_gma": [False, True],
        "lenc": [False, True],
        "aec_gain": list_range(30),
        "aec_value": list_range(0, 1200, 50),
        "wb_mode": list_range(0, 5),
    },
}

with open("htdocs/metadata.js", "w", encoding="utf-8") as f:
    print(end="tunables = ", file=f)
    json.dump(metadata, f, indent=4)
    print(";", file=f)
