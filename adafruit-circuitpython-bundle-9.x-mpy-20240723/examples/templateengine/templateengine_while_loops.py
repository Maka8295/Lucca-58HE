# SPDX-FileCopyrightText: Copyright (c) 2023 Michał Pokusa
#
# SPDX-License-Identifier: Unlicense

from random import randint

from adafruit_templateengine import render_string


template = r"""
<!DOCTYPE html>
<html>
    <head>
        <title>While loops</title>
    </head>
    <body>
        Before rolling a 6, the dice rolled:
        <ul>
        {% while (dice_roll := context["random_dice_roll"]()) != 6 %}
            <li>{{ dice_roll }}</li>
        {% endwhile %}
        </ul>
    </body>
</html>
"""

context = {"random_dice_roll": lambda: randint(1, 6)}

print(render_string(template, context))
