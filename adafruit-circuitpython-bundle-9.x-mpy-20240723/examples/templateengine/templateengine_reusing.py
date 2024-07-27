# SPDX-FileCopyrightText: Copyright (c) 2023 Michał Pokusa
#
# SPDX-License-Identifier: Unlicense

from adafruit_templateengine import Template, render_string


template_string = r"""
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

other_template_string = r"""
<footer>
    <p>Goodbye, {{ context.get("name") or "Anonymous User" }}!</p>
</footer>
"""

# Manually create a Template object
template = Template(template_string)  # Creates a template object
print(template.render({"name": "John"}))  # Reuses the Template object
print(template.render({"name": "Alex"}))  # Reuses the Template object

# Using the `render_string` function
print(
    render_string(template_string, {"name": "John"})
)  # Creates a new Template object and saves it
print(render_string(template_string, {"name": "Alex"}))  # Reuses the Template object


# Using the `render_string` function, but without caching
print(
    render_string(other_template_string, {"name": "John"}, cache=False)
)  # Creates a new Template object and does not save it
print(
    render_string(other_template_string, {"name": "Alex"}, cache=False)
)  # Creates a new Template object a second time and does not save it
