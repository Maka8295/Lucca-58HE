# SPDX-FileCopyrightText: Copyright (c) 2023 Michał Pokusa
#
# SPDX-License-Identifier: Unlicense

from adafruit_templateengine import render_string


template = r"""
<!DOCTYPE html>
<html>
    <head>
        <title>Executing Python code</title>
    </head>
    <body>

        {% exec name = "jake" %}
        We defined a name: {{ name }}</br>

        {% exec name = (name[0].upper() + name[1:].lower()) if name else "" %}
        First letter was capitalized: {{ name }}</br>

        {% exec name = list(name) %}
        Not it got converted to a list: {{ name }}</br>

        {% exec name = list(reversed(name)) %}
        And reverse-sorted: {{ name }}</br>

        {% for letter in name %}
            {% if letter != "a" %}
                {% if letter == "k" %}
                    Skip a letter... e.g. "{{ letter }}"</br>
                    {% exec continue %}
                {% endif %}
                We can iterate over it: "{{ letter }}"</br>
            {% else %}
                And break the loop when we find an "a" letter.</br>
                {% exec break %}
            {% endif %}
        {% endfor %}
    </body>
</html>
"""

print(render_string(template))
