# SPDX-FileCopyrightText: 2021 Stefan Krüger
#
# SPDX-License-Identifier: MIT
#############################
"""
This is a basic demonstration of a Cartesian widget for line-ploting
"""

import time
import board
import displayio
from adafruit_displayio_layout.widgets.cartesian import Cartesian

# create the display on the PyPortal or Clue or PyBadge(for example)
display = board.DISPLAY
# otherwise change this to setup the display
# for display chip driver and pinout you have (e.g. ILI9341)

# pybadge display:  160x128
# Create a Cartesian widget
# https://circuitpython.readthedocs.io/projects/displayio-layout/en/latest/api.html#module-adafruit_displayio_layout.widgets.cartesian
my_plane = Cartesian(
    x=15,  # x position for the plane
    y=2,  # y plane position
    width=140,  # display width
    height=105,  # display height
    xrange=(0, 10),  # x range
    yrange=(0, 10),  # y range
)

my_group = displayio.Group()
my_group.append(my_plane)
display.root_group = my_group  # add high level Group to the display

data = [
    # (0, 0),  # we do this point manually - so we have no wait...
    (1, 1),
    (2, 1),
    (2, 2),
    (3, 3),
    (4, 3),
    (4, 4),
    (5, 5),
    (6, 5),
    (6, 6),
    (7, 7),
    (8, 7),
    (8, 8),
    (9, 9),
    (10, 9),
    (10, 10),
]

print("examples/displayio_layout_cartesian_lineplot.py")

# first point without a wait.
my_plane.add_plot_line(0, 0)
for x, y in data:
    my_plane.add_plot_line(x, y)
    time.sleep(0.5)

while True:
    pass
