# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
import displayio
import terminalio
from adafruit_display_text.label import Label
from simpleio import map_range
import adafruit_mlx90640

number_of_colors = 64  # Number of color in the gradian
last_color = number_of_colors - 1  # Last color in palette
palette = displayio.Palette(number_of_colors)  # Palette with all our colors

## Heatmap code inspired from: http://www.andrewnoske.com/wiki/Code_-_heatmaps_and_color_gradients
color_A = [
    [0, 0, 0],
    [0, 0, 255],
    [0, 255, 255],
    [0, 255, 0],
    [255, 255, 0],
    [255, 0, 0],
    [255, 255, 255],
]
color_B = [[0, 0, 255], [0, 255, 255], [0, 255, 0], [255, 255, 0], [255, 0, 0]]
color_C = [[0, 0, 0], [255, 255, 255]]
color_D = [[0, 0, 255], [255, 0, 0]]

color = color_B
NUM_COLORS = len(color)


def MakeHeatMapColor():
    for c in range(number_of_colors):
        value = c * (NUM_COLORS - 1) / last_color
        idx1 = int(value)  # Our desired color will be after this index.
        if idx1 == value:  # This is the corner case
            red = color[idx1][0]
            green = color[idx1][1]
            blue = color[idx1][2]
        else:
            idx2 = idx1 + 1  # ... and before this index (inclusive).
            fractBetween = value - idx1  # Distance between the two indexes (0-1).
            red = int(
                round((color[idx2][0] - color[idx1][0]) * fractBetween + color[idx1][0])
            )
            green = int(
                round((color[idx2][1] - color[idx1][1]) * fractBetween + color[idx1][1])
            )
            blue = int(
                round((color[idx2][2] - color[idx1][2]) * fractBetween + color[idx1][2])
            )
        palette[c] = (0x010000 * red) + (0x000100 * green) + (0x000001 * blue)


MakeHeatMapColor()

# Bitmap for colour coded thermal value
image_bitmap = displayio.Bitmap(32, 24, number_of_colors)
# Create a TileGrid using the Bitmap and Palette
image_tile = displayio.TileGrid(image_bitmap, pixel_shader=palette)
# Create a Group that scale 32*24 to 128*96
image_group = displayio.Group(scale=4)
image_group.append(image_tile)

scale_bitmap = displayio.Bitmap(number_of_colors, 1, number_of_colors)
# Create a Group Scale must be 128 divided by number_of_colors
scale_group = displayio.Group(scale=2)
scale_tile = displayio.TileGrid(scale_bitmap, pixel_shader=palette, x=0, y=60)
scale_group.append(scale_tile)

for i in range(number_of_colors):
    scale_bitmap[i, 0] = i  # Fill the scale with the palette gradian

# Create the super Group
group = displayio.Group()

min_label = Label(terminalio.FONT, color=palette[0], x=0, y=110)
max_label = Label(terminalio.FONT, color=palette[last_color], x=80, y=110)

# Add all the sub-group to the SuperGroup
group.append(image_group)
group.append(scale_group)
group.append(min_label)
group.append(max_label)

# Add the SuperGroup to the Display
board.DISPLAY.root_group = group

min_t = 20  # Initial minimum temperature range, before auto scale
max_t = 37  # Initial maximum temperature range, before auto scale

i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C")
print([hex(i) for i in mlx.serial_number])

# mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_4_HZ

frame = [0] * 768

while True:
    stamp = time.monotonic()
    try:
        mlx.getFrame(frame)
    except ValueError:
        # these happen, no biggie - retry
        continue

    #    print("Time for data aquisition: %0.2f s" % (time.monotonic()-stamp))

    mini = frame[0]  # Define a min temperature of current image
    maxi = frame[0]  # Define a max temperature of current image

    for h in range(24):
        for w in range(32):
            t = frame[h * 32 + w]
            if t > maxi:
                maxi = t
            if t < mini:
                mini = t
            image_bitmap[w, (23 - h)] = int(map_range(t, min_t, max_t, 0, last_color))

    min_label.text = "%0.2f" % (min_t)

    max_string = "%0.2f" % (max_t)
    max_label.x = 120 - (5 * len(max_string))  # Tricky calculation to left align
    max_label.text = max_string

    min_t = mini  # Automatically change the color scale
    max_t = maxi
#    print((mini, maxi))           # Use this line to display min and max graph in Mu
#    print("Total time for aquisition and display %0.2f s" % (time.monotonic()-stamp))
