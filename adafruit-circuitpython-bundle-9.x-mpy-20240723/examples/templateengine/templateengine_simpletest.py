# SPDX-FileCopyrightText: Copyright (c) 2023 Michał Pokusa
#
# SPDX-License-Identifier: Unlicense

from adafruit_templateengine import render_string


template = r"""
<!DOCTYPE html>
<html>
    <head>
        <title>Hello</title>
    </head>
    <body>
        <p>Hello, {{ context.get("name") or "Anonymous User" }}!</p>
    </body>
</html>
"""

context = {"name": ""}  # Put your name here

print(render_string(template, context))
