# SPDX-FileCopyrightText: 2021 Jose David M.
#
# SPDX-License-Identifier: MIT
#############################
"""
This is an advanced demonstration of the display_text library capabilities
"""

import time
import board
import displayio
import terminalio
import fontio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label, bitmap_label

display = board.DISPLAY
main_group = displayio.Group()
MEDIUM_FONT = bitmap_font.load_font("fonts/LeagueSpartan-Bold-16.bdf")
BIG_FONT = bitmap_font.load_font("fonts/LibreBodoniv2002-Bold-27.bdf")
TIME_PAUSE = 2

bitmap = displayio.Bitmap(4, display.width, 2)
palette = displayio.Palette(2)
palette[0] = 0x004400
palette[1] = 0x00FFFF
horizontal_line = displayio.TileGrid(bitmap, pixel_shader=palette, x=155, y=0)
main_group.append(horizontal_line)

bitmap = displayio.Bitmap(display.width, 4, 2)
vertical_line = displayio.TileGrid(bitmap, pixel_shader=palette, x=0, y=110)
main_group.append(vertical_line)

# Tests
text_area = label.Label(terminalio.FONT, text="Circuit Python")
main_group.append(text_area)
display.root_group = main_group
time.sleep(TIME_PAUSE)

# Testing position setter
text_area.x = 10
text_area.y = 10
display.root_group = main_group
time.sleep(TIME_PAUSE)

# Testing creating label with initial position
text_area.text = "Testing initiating without text"
try:
    text_middle = label.Label(terminalio.FONT)
except SyntaxError:
    print("Fail setting-up label without text")
    warning_text = label.Label(
        BIG_FONT,
        text="Test Fail",
        x=display.width // 2,
        y=display.height // 4,
        background_color=0x004499,
    )
    main_group.append(warning_text)
display.root_group = main_group
time.sleep(TIME_PAUSE)

text_area.text = "Testing Position"
text_middle = label.Label(
    terminalio.FONT, text="Circuit", x=display.width // 2, y=display.height // 2
)
main_group.append(text_middle)
display.root_group = main_group
time.sleep(TIME_PAUSE)

# Testing Text Setter
text_area.text = "Testing Changing Text"
text_middle.text = "Python"
display.root_group = main_group
time.sleep(TIME_PAUSE)

# Testing a and y getter and setter
text_area.text = "Testing Changing Position"
text_middle.x = text_middle.x - 50
text_middle.y = text_middle.y - 50
display.root_group = main_group
time.sleep(TIME_PAUSE)

# Testing font Getter and setter
text_area.text = "Testing Changing FONT"
if isinstance(text_middle.font, fontio.BuiltinFont):
    text_middle.font = MEDIUM_FONT
display.root_group = main_group
time.sleep(TIME_PAUSE)

# Once this working we create another label with all the initial specs
main_group.pop()

# Testing Color
text_area.text = "Testing Color"
text_initial_specs = label.Label(
    MEDIUM_FONT,
    text="Circuit Python",
    x=display.width // 2,
    y=display.height // 2,
)
main_group.append(text_initial_specs)
display.root_group = main_group
time.sleep(TIME_PAUSE)

text_initial_specs.color = 0x004400
display.root_group = main_group
time.sleep(TIME_PAUSE)
main_group.pop()

# Testing Background Color
text_area.text = "Testing Background Color"
text_initial_specs = label.Label(
    MEDIUM_FONT,
    text="CircuitPython",
    x=display.width // 2,
    y=display.height // 2,
    color=0xFFFFFF,
)
main_group.append(text_initial_specs)
display.root_group = main_group
time.sleep(TIME_PAUSE)

text_initial_specs.background_color = 0x990099
display.root_group = main_group
time.sleep(TIME_PAUSE)
main_group.pop()

# Testing Background Color
text_area.text = "Testing Background Tight"
text_initial_specs = label.Label(
    BIG_FONT,
    text="aaaaq~",
    x=0,
    y=display.height // 2,
    color=0xFFFFFF,
    background_color=0x990099,
    background_tight=True,
)
main_group.append(text_initial_specs)
text_initial_specs = label.Label(
    BIG_FONT,
    text="aaaaq~",
    x=90,
    y=display.height // 2,
    color=0xFFFFFF,
    background_color=0x990099,
    background_tight=False,
)
main_group.append(text_initial_specs)
display.root_group = main_group
time.sleep(TIME_PAUSE)
main_group.pop()
main_group.pop()

# Testing Padding
text_area.text = "Testing Padding"
text_initial_specs = label.Label(
    BIG_FONT,
    text="CircuitPython",
    x=display.width // 4,
    y=display.height // 2,
    color=0xFFFFFF,
    background_color=0x990099,
    padding_right=10,
    padding_top=10,
    padding_bottom=10,
    padding_left=10,
)
main_group.append(text_initial_specs)
display.root_group = main_group
time.sleep(TIME_PAUSE)
main_group.pop()

# Testing Anchor Point/ Anchored Position
text_area.text = "Testing Anchor Point/Anchored Position"
text_initial_specs = label.Label(
    MEDIUM_FONT,
    text="CircuitPython",
    x=display.width // 2,
    y=display.height // 2,
    color=0xFFFFFF,
    background_color=0x990099,
    padding_right=10,
    padding_top=10,
    padding_bottom=10,
    padding_left=10,
)
main_group.append(text_initial_specs)
display.root_group = main_group
time.sleep(TIME_PAUSE)

try:
    text_initial_specs.anchored_position = (100, 100)
    text_initial_specs.anchor_point = (0.5, 0.5)

except TypeError:
    print("Test is failing here")
    main_group.pop()
    warning_text = label.Label(
        BIG_FONT,
        text="Test Fail",
        x=display.width // 2,
        y=display.height // 4,
        background_color=0x004499,
    )
    main_group.append(warning_text)
    time.sleep(TIME_PAUSE)
    display.root_group = main_group

main_group.pop()

# Testing Scale
text_area.text = "Testing Scale"
text_initial_specs = label.Label(
    MEDIUM_FONT,
    text="CircuitPython",
    x=display.width // 2,
    y=display.height // 2,
    color=0xFFFFFF,
    background_color=0x990099,
    padding_right=10,
    padding_top=10,
    padding_bottom=10,
    padding_left=10,
    anchored_position=(display.width // 2, display.height // 2),
    anchor_point=(0.5, 0.5),
)
main_group.append(text_initial_specs)
display.root_group = main_group
time.sleep(TIME_PAUSE)

text_initial_specs.scale = 2
display.root_group = main_group
time.sleep(TIME_PAUSE)
main_group.pop()

# Testing Base Alignment
text_area.text = "Testing Base Alignment"
text_initial_specs = label.Label(
    MEDIUM_FONT,
    text="python",
    x=display.width // 2,
    y=display.height // 2,
    color=0xFFFFFF,
    background_color=0x990099,
    base_alignment=True,
)
main_group.append(text_initial_specs)
text_initial_specs = label.Label(
    BIG_FONT,
    text="circuit",
    x=display.width // 2 - 100,
    y=display.height // 2,
    color=0xFFFFFF,
    background_color=0x990099,
    base_alignment=True,
)
main_group.append(text_initial_specs)
display.root_group = main_group
time.sleep(TIME_PAUSE)
main_group.pop()
main_group.pop()

# Testing Direction
text_area.text = "Testing Direction-UPR"
text_initial_specs = label.Label(
    MEDIUM_FONT,
    text="CircuitPython",
    x=display.width // 2,
    y=display.height // 2,
    color=0xFFFFFF,
    background_color=0x990099,
    padding_right=10,
    padding_top=10,
    padding_bottom=10,
    padding_left=10,
    anchored_position=(display.width // 2, display.height // 2),
    anchor_point=(0.5, 0.5),
    label_direction="UPR",
)
main_group.append(text_initial_specs)
display.root_group = main_group
time.sleep(TIME_PAUSE)
main_group.pop()

text_area.text = "Testing Direction-DWR"
text_initial_specs = label.Label(
    MEDIUM_FONT,
    text="CircuitPython",
    x=display.width // 2,
    y=display.height // 2,
    color=0xFFFFFF,
    background_color=0x990099,
    padding_right=10,
    padding_top=10,
    padding_bottom=10,
    padding_left=10,
    anchored_position=(display.width // 2, display.height // 2),
    anchor_point=(0.5, 0.5),
    label_direction="DWR",
)
main_group.append(text_initial_specs)
display.root_group = main_group
time.sleep(TIME_PAUSE)
main_group.pop()

text_area.text = "Testing Direction-TTB"
text_initial_specs = label.Label(
    MEDIUM_FONT,
    text="CircuitPython",
    x=display.width // 2,
    y=display.height // 2,
    color=0xFFFFFF,
    background_color=0x990099,
    padding_right=10,
    padding_top=10,
    padding_bottom=10,
    padding_left=10,
    anchored_position=(display.width // 2, display.height // 2),
    anchor_point=(0.5, 0.5),
    label_direction="TTB",
)
main_group.append(text_initial_specs)
display.root_group = main_group
time.sleep(TIME_PAUSE)
main_group.pop()

text_area.text = "Testing Direction-RTL"
text_initial_specs = label.Label(
    MEDIUM_FONT,
    text="CircuitPython",
    x=display.width // 2,
    y=display.height // 2,
    color=0xFFFFFF,
    background_color=0x990099,
    padding_right=10,
    padding_top=10,
    padding_bottom=10,
    padding_left=10,
    anchored_position=(display.width // 2, display.height // 2),
    anchor_point=(0.5, 0.5),
    label_direction="RTL",
)
main_group.append(text_initial_specs)
display.root_group = main_group
time.sleep(TIME_PAUSE)
main_group.pop()

main_group.pop()

# Testing creating label with initial position
display.root_group = main_group
time.sleep(TIME_PAUSE)
text_area = bitmap_label.Label(terminalio.FONT, text="Circuit Python")
main_group.append(text_area)
display.root_group = main_group
time.sleep(TIME_PAUSE)
# Testing position setter
text_area.x = 10
text_area.y = 10
display.root_group = main_group
time.sleep(TIME_PAUSE)
text_area.text = "Testing initiating without text"
try:
    text_middle = label.Label(terminalio.FONT)
except TypeError:
    print("Fail setting-up label without text")
    warning_text = label.Label(
        BIG_FONT,
        text="Test Fail",
        x=display.width // 2,
        y=display.height // 4,
        background_color=0x004499,
    )
    main_group.append(warning_text)

# Testing creating label with initial position
text_area.text = "Testing Position"
text_middle = bitmap_label.Label(
    terminalio.FONT, text="Circuit", x=display.width // 2, y=display.height // 2
)
main_group.append(text_middle)
display.root_group = main_group
time.sleep(TIME_PAUSE)

# Testing Text Setter
text_area.text = "Testing Changing Text"
text_middle.text = "Python"
display.root_group = main_group
time.sleep(TIME_PAUSE)

# Testing a and y getter and setter
text_area.text = "Testing Changing Position"
text_middle.x = text_middle.x - 50
text_middle.y = text_middle.y - 50
display.root_group = main_group
time.sleep(TIME_PAUSE)

# Testing font Getter and setter
text_area.text = "Testing Changing FONT"
if isinstance(text_middle.font, fontio.BuiltinFont):
    print("Font was BuiltinFont")
    text_middle.font = MEDIUM_FONT
display.root_group = main_group
time.sleep(TIME_PAUSE)

# Once this working we create another label with all the initial specs
main_group.pop()

# Testing Color
text_area.text = "Testing Color"
text_initial_specs = bitmap_label.Label(
    MEDIUM_FONT,
    text="Circuit Python",
    x=display.width // 2,
    y=display.height // 2,
)
main_group.append(text_initial_specs)
display.root_group = main_group
time.sleep(TIME_PAUSE)

text_initial_specs.color = 0x004400
display.root_group = main_group
time.sleep(TIME_PAUSE)
main_group.pop()

# Testing Background Color
text_area.text = "Testing Background Color"
text_initial_specs = bitmap_label.Label(
    MEDIUM_FONT,
    text="CircuitPython",
    x=display.width // 2,
    y=display.height // 2,
    color=0xFFFFFF,
)
main_group.append(text_initial_specs)
display.root_group = main_group
time.sleep(TIME_PAUSE)

text_initial_specs.background_color = 0x990099
display.root_group = main_group
time.sleep(TIME_PAUSE)
main_group.pop()

# Testing Background Color
text_area.text = "Testing Background Tight"
text_initial_specs = bitmap_label.Label(
    BIG_FONT,
    text="aaaaq~",
    x=0,
    y=display.height // 2,
    color=0xFFFFFF,
    background_color=0x990099,
    background_tight=True,
)
main_group.append(text_initial_specs)
text_initial_specs = bitmap_label.Label(
    BIG_FONT,
    text="aaaaq~",
    x=90,
    y=display.height // 2,
    color=0xFFFFFF,
    background_color=0x990099,
    background_tight=False,
)
main_group.append(text_initial_specs)
display.root_group = main_group
time.sleep(TIME_PAUSE)
main_group.pop()
main_group.pop()

# Testing Padding
text_area.text = "Testing Padding"
text_initial_specs = bitmap_label.Label(
    BIG_FONT,
    text="CircuitPython",
    x=display.width // 4,
    y=display.height // 2,
    color=0xFFFFFF,
    background_color=0x990099,
    padding_right=10,
    padding_top=10,
    padding_bottom=10,
    padding_left=10,
)
main_group.append(text_initial_specs)
display.root_group = main_group
time.sleep(TIME_PAUSE)
main_group.pop()

# Testing Anchor Point/ Anchored Position
text_area.text = "Testing Anchor Point/Anchored Position"
text_initial_specs = bitmap_label.Label(
    MEDIUM_FONT,
    text="CircuitPython",
    x=display.width // 2,
    y=display.height // 2,
    color=0xFFFFFF,
    background_color=0x990099,
    padding_right=10,
    padding_top=10,
    padding_bottom=10,
    padding_left=10,
)
main_group.append(text_initial_specs)
display.root_group = main_group
time.sleep(TIME_PAUSE)

try:
    text_initial_specs.anchored_position = (100, 100)
    text_initial_specs.anchor_point = (0.5, 0.5)

except TypeError:
    print("Test is failing here")
    main_group.pop()
    warning_text = bitmap_label.Label(
        BIG_FONT,
        text="Test Fail",
        x=display.width // 2,
        y=display.height // 4,
        background_color=0x004499,
    )
    main_group.append(warning_text)
    time.sleep(TIME_PAUSE)
    display.root_group = main_group

main_group.pop()

# Testing Scale
text_area.text = "Testing Scale"
text_initial_specs = bitmap_label.Label(
    MEDIUM_FONT,
    text="CircuitPython",
    x=display.width // 2,
    y=display.height // 2,
    color=0xFFFFFF,
    background_color=0x990099,
    padding_right=10,
    padding_top=10,
    padding_bottom=10,
    padding_left=10,
    anchored_position=(display.width // 2, display.height // 2),
    anchor_point=(0.5, 0.5),
)
main_group.append(text_initial_specs)
display.root_group = main_group
time.sleep(TIME_PAUSE)

text_initial_specs.scale = 2
display.root_group = main_group
time.sleep(TIME_PAUSE)
main_group.pop()

# Testing Base Alignment
text_area.text = "Testing Base Alignment"
text_initial_specs = bitmap_label.Label(
    MEDIUM_FONT,
    text="python",
    x=display.width // 2,
    y=display.height // 2,
    color=0xFFFFFF,
    background_color=0x990099,
    base_alignment=True,
)
main_group.append(text_initial_specs)
text_initial_specs = bitmap_label.Label(
    BIG_FONT,
    text="circuit",
    x=display.width // 2 - 100,
    y=display.height // 2,
    color=0xFFFFFF,
    background_color=0x990099,
    base_alignment=True,
)
main_group.append(text_initial_specs)
display.root_group = main_group
time.sleep(TIME_PAUSE)
main_group.pop()
main_group.pop()

# Testing Direction
text_area.text = "Testing Direction-UPR"
text_initial_specs = bitmap_label.Label(
    MEDIUM_FONT,
    text="CircuitPython",
    x=display.width // 2,
    y=display.height // 2,
    color=0xFFFFFF,
    background_color=0x990099,
    padding_right=10,
    padding_top=10,
    padding_bottom=10,
    padding_left=10,
    anchored_position=(display.width // 2, display.height // 2),
    anchor_point=(0.5, 0.5),
    label_direction="UPR",
)
main_group.append(text_initial_specs)
display.root_group = main_group
time.sleep(TIME_PAUSE)
main_group.pop()

text_area.text = "Testing Direction-DWR"
text_initial_specs = bitmap_label.Label(
    MEDIUM_FONT,
    text="CircuitPython",
    x=display.width // 2,
    y=display.height // 2,
    color=0xFFFFFF,
    background_color=0x990099,
    padding_right=10,
    padding_top=10,
    padding_bottom=10,
    padding_left=10,
    anchored_position=(display.width // 2, display.height // 2),
    anchor_point=(0.5, 0.5),
    label_direction="DWR",
)
main_group.append(text_initial_specs)
display.root_group = main_group
time.sleep(TIME_PAUSE)
main_group.pop()

text_area.text = "Testing Direction-UPD"
text_initial_specs = bitmap_label.Label(
    MEDIUM_FONT,
    text="CircuitPython",
    x=display.width // 2,
    y=display.height // 2,
    color=0xFFFFFF,
    background_color=0x990099,
    padding_right=10,
    padding_top=10,
    padding_bottom=10,
    padding_left=10,
    anchored_position=(display.width // 2, display.height // 2),
    anchor_point=(0.5, 0.5),
    label_direction="UPD",
)
main_group.append(text_initial_specs)
display.root_group = main_group
time.sleep(TIME_PAUSE)
main_group.pop()

text_area.text = "Testing Direction-RTL"
text_initial_specs = bitmap_label.Label(
    MEDIUM_FONT,
    text="CircuitPython",
    x=display.width // 2,
    y=display.height // 2,
    color=0xFFFFFF,
    background_color=0x990099,
    padding_right=10,
    padding_top=10,
    padding_bottom=10,
    padding_left=10,
    anchored_position=(display.width // 2, display.height // 2),
    anchor_point=(0.5, 0.5),
    label_direction="RTL",
)
main_group.append(text_initial_specs)
display.root_group = main_group
time.sleep(TIME_PAUSE)
main_group.pop()

text_area.text = "Finished"
print("Tests finished")
