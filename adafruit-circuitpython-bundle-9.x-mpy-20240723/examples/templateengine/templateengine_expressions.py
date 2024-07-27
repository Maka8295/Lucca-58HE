# SPDX-FileCopyrightText: Copyright (c) 2023 Michał Pokusa
#
# SPDX-License-Identifier: Unlicense

from adafruit_templateengine import render_string


template = r"""
<!DOCTYPE html>
<html>
    <head>
        <title>Expressions</title>
    </head>
    <body>
        Your name is {{ context["name"] }} and it is {{ len(context["name"]) }} characters long.

        If I were to shout your name, it would look like this: {{ context["name"].upper() }}!.

        You are {{ context["age"] }} years old,
        which means that you {{ "are not" if context["age"] <= 18 else "are" }} an adult.

        You are also {{ 100 - context["age"] }} years away from being 100 years old.
    </body>
</html>
"""

context = {
    "name": "John Doe",
    "age": 23,
}

print(render_string(template, context))
