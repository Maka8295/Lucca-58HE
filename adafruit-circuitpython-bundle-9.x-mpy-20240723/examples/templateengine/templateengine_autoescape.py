# SPDX-FileCopyrightText: Copyright (c) 2023 Michał Pokusa
#
# SPDX-License-Identifier: Unlicense

from adafruit_templateengine import render_template

# By default autoescape is enabled for HTML entities
print(render_template("./examples/autoescape.html"))
