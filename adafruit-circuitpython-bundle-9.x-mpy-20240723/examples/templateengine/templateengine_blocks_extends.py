# SPDX-FileCopyrightText: Copyright (c) 2023 Michał Pokusa
#
# SPDX-License-Identifier: Unlicense

from adafruit_templateengine import render_template

context = {
    "items": [
        {"name": "Apple", "price": 10},
        {"name": "Orange", "price": 20},
        {"name": "Lettuce", "price": 30},
    ],
}

print(render_template("./examples/child.html", context))
