# SPDX-FileCopyrightText: Copyright (c) 2023 Michał Pokusa
#
# SPDX-License-Identifier: Unlicense

from adafruit_templateengine import render_string


template = r"""
<!DOCTYPE html>
<html>
    <head>
        <title>For loops</title>
    </head>
    <body>

        Shopping list:
        <ul>
            {% for item in context["items"] %}
                <li>{{ item["name"] }} - ${{ item["price"] }}</li>
            {% empty %}
                <li>There are no items on the list.</li>
            {% endfor %}
        </ul>
    </body>
</html>
"""

context = {
    "items": [
        {"name": "Apple", "price": 10},
        {"name": "Orange", "price": 20},
        {"name": "Lettuce", "price": 30},
    ],
}

print(render_string(template, context))
