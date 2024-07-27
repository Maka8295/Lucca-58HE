# SPDX-FileCopyrightText: Copyright (c) 2023 Michał Pokusa
#
# SPDX-License-Identifier: Unlicense

from adafruit_templateengine import render_string


template = r"""
<!DOCTYPE html>
<html>
    <head>
        <title>If statements</title>
    </head>
    <body>
        {% if context["is_admin"] %}
            <p>You are an admin.</p>
        {% elif context["is_user"] %}
            <p>You are a user.</p>
        {% else %}
            <p>You are a guest.</p>
        {% endif %}
    </body>
</html>
"""

context = {
    "is_admin": True,
    "is_user": True,
}

print(render_string(template, context))
