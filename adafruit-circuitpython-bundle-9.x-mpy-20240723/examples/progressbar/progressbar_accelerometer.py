# SPDX-FileCopyrightText: 2021 Jose David M.
# SPDX-License-Identifier: MIT
"""
With this example you would be able to use the progress bar to display accelerometer data
in the X and Y directions
"""
import time
import displayio
import board
from adafruit_progressbar.horizontalprogressbar import (
    HorizontalProgressBar,
    HorizontalFillDirection,
)
from adafruit_progressbar.verticalprogressbar import (
    VerticalProgressBar,
    VerticalFillDirection,
)

# This data is used to show library capability. You could use an actual accelerometer
# This data was extracted from an Adafruit MSA301 Triple Axis Accelerometer
fake__accel_data = [
    (-0.071821, 1.450790, 9.533077),
    (-0.105338, 1.939175, 9.111725),
    (-0.306437, 2.906367, 9.178761),
    (-0.062245, 3.504878, 8.776562),
    (-0.143643, 4.792873, 8.091862),
    (-0.172371, 5.520662, 7.838097),
    (0.014364, 6.176630, 7.426321),
    (-0.205888, 7.526871, 6.200571),
    (-0.090974, 7.905128, 5.491934),
    (-0.445292, 8.216354, 5.118464),
    (-0.110126, 8.872322, 4.017202),
    (-0.344742, 9.542652, 1.498671),
    (-0.076609, 9.580959, -0.033517),
    (-0.158007, 9.518715, -1.273631),
    (0.282497, 9.446892, -2.877639),
    (-0.004788, 9.063847, -3.409117),
    (-0.153219, 8.599400, -4.630077),
    (-0.071821, 8.020042, -6.382517),
    (0.655968, 6.722471, -6.937935),
    (0.464444, 5.740913, -7.771063),
    (1.034226, 4.189575, -8.905838),
    (1.369392, 1.675830, -8.340843),
    (2.149850, -1.426849, -9.178761),
    (2.384466, -3.662886, -8.834019),
    (2.417983, -5.223801, -7.957798),
    (2.336586, -7.900341, -5.482357),
    (2.106757, -9.231426, -4.194363),
    (1.948751, -3.945382, -9.288883),
    (0.588934, 0.062245, -9.643204),
    (0.430928, 2.250400, -9.360706),
    (-0.402199, 7.249161, -6.176630),
    (-0.871432, 8.197201, -5.003550),
    (0.373471, 8.829227, -3.696402),
    (0.584146, 9.662357, -1.287995),
    (0.114914, 9.940063, 0.536266),
    (-0.201100, 9.207489, 2.848910),
    (-0.181947, 8.589825, 5.314775),
    (-0.517113, 5.573332, 7.598692),
    (-0.497961, 3.160136, 9.092575),
    (-0.114914, -1.541763, 9.940063),
    (-0.555418, -5.099310, 7.727970),
    (-0.387835, -7.091154, 7.095942),
    (0.162795, -8.652069, 4.768932),
    (0.531477, -8.934566, 0.751729),
    (0.775670, -9.542652, -4.141693),
    (1.809896, -7.177340, -7.282679),
    (0.957617, -2.868063, -9.308037),
    (1.450790, -0.866643, -9.571381),
    (1.039014, -0.660756, -9.758118),
    (0.914524, -4.907787, -8.379150),
    (1.302359, -8.120594, -5.870192),
    (1.043803, -9.916122, 2.365314),
    (1.086895, -8.412666, 5.223801),
    (2.034936, -5.942015, 7.488565),
    (2.010996, -2.767513, 9.140453),
    (0.397411, -2.322221, 9.130878),
    (-2.025360, -2.398830, 9.116512),
    (-2.824970, -2.264764, 8.896263),
    (-4.395462, -2.001419, 8.259445),
    (-5.640364, -1.220962, 7.569963),
    (-7.000181, -0.746941, 6.679379),
    (-8.077499, -0.004788, 5.338715),
    (-9.001598, 0.421352, 2.585566),
    (-9.408588, 1.106048, 1.053379),
    (-9.097363, 2.283916, -1.589644),
    (-8.522793, 2.714845, -3.021282),
    (-7.991314, 3.083527, -4.505589),
    (-6.416035, 3.720343, -6.732048),
    (-6.186207, 3.562336, -5.788795),
    (-3.289414, 3.428269, -8.254658),
    (-1.110836, 3.787375, -8.944141),
    (1.082107, 3.270263, -9.059055),
    (1.565704, 3.820892, -8.446182),
    (2.212095, 3.763435, -8.221142),
    (3.030858, 4.175211, -8.029617),
    (-2.365314, 2.633447, -8.221142),
    (-5.372232, 2.188155, -7.445473),
    (-8.465336, 2.116334, -4.577410),
    (-9.432529, 1.388545, 0.541054),
    (-6.957088, 1.623161, 6.085657),
    (-4.735416, 0.751729, 8.992023),
    (-1.800320, 2.063664, 9.762905),
    (-0.153219, -1.795532, 9.657566),
    (5.764854, -3.801740, 6.775141),
    (9.470833, -2.240824, 2.777089),
    (9.925701, -1.000710, -1.915234),
    (8.685585, 0.277709, -4.347582),
    (9.676720, -0.459656, -0.521901),
    (9.719814, -0.689484, 1.584856),
    (8.541943, -1.503459, 4.160847),
    (7.608267, -1.824261, 5.865404),
    (5.817524, -1.446002, 6.770353),
    (3.887925, -1.991844, 8.671223),
    (1.805108, -2.039724, 9.303249),
    (0.593723, -1.690194, 9.518715),
    (0.852279, -2.087605, 9.427738),
    (1.206597, -1.857777, 9.226639),
    (0.392623, -2.255188, 9.193123),
    (-2.475440, -2.154638, 9.173969),
    (-3.677250, -8.288174, 3.198441),
    (-0.981558, -2.944673, 8.977661),
    (1.517823, 3.409117, 8.977661),
    (2.796242, 5.989895, 5.807947),
    (4.151270, -2.552050, 9.418163),
    (4.242243, -9.844303, 1.694982),
    (5.946802, -3.543183, 6.890055),
    (7.028910, -4.462496, 4.199150),
    (-1.694982, -6.655439, 6.430399),
    (0.703849, -3.112255, 8.685585),
    (1.340664, 4.342793, 8.053558),
    (1.627949, 9.920914, -0.608087),
    (6.985817, 0.517113, 7.517294),
    (5.434477, -5.372232, 5.994682),
    (4.165634, -6.224510, 8.082287),
    (0.847491, -4.677959, 9.509136),
    (3.476150, -4.812025, 7.421532),
]
display = board.DISPLAY
main_group = displayio.Group()
display.root_group = main_group

color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x990099

background = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
main_group.append(background)

# Accelerometer Properties. Normally accelerometer well calibrated
# Will give a maximum output of 10 mts / s**2
VALUES_X = (-10, 10)
VALUES_Y = (-10, 10)

# Horizontal Bar Properties
HORIZONTAL_BAR_X_ORIGIN = 10
HORIZONTAL_BAR_Y_ORIGIN = 30
HORIZONTAL_BAR_WIDTH = display.width // 4
HORIZONTAL_BAR_HEIGHT = 30

# Vertical Bar Properties
VERTICAL_BAR_HEIGHT = display.height // 4
VERTICAL_BAR_WIDTH = 30

# We create our bar displays
left_horizontal_bar = HorizontalProgressBar(
    (HORIZONTAL_BAR_X_ORIGIN, HORIZONTAL_BAR_Y_ORIGIN),
    (HORIZONTAL_BAR_WIDTH, HORIZONTAL_BAR_HEIGHT),
    min_value=0,
    max_value=-VALUES_X[0],
    direction=HorizontalFillDirection.RIGHT_TO_LEFT,
)
main_group.append(left_horizontal_bar)

right_horizontal_bar = HorizontalProgressBar(
    (HORIZONTAL_BAR_X_ORIGIN + HORIZONTAL_BAR_WIDTH, HORIZONTAL_BAR_Y_ORIGIN),
    (HORIZONTAL_BAR_WIDTH, HORIZONTAL_BAR_HEIGHT),
    min_value=0,
    max_value=VALUES_X[1],
    direction=HorizontalFillDirection.LEFT_TO_RIGHT,
)
main_group.append(right_horizontal_bar)


top_vertical_bar = VerticalProgressBar(
    (HORIZONTAL_BAR_X_ORIGIN + 2 * HORIZONTAL_BAR_WIDTH + 20, HORIZONTAL_BAR_Y_ORIGIN),
    (VERTICAL_BAR_WIDTH, VERTICAL_BAR_HEIGHT),
    min_value=0,
    max_value=VALUES_Y[1],
    direction=VerticalFillDirection.BOTTOM_TO_TOP,
)
main_group.append(top_vertical_bar)

bottom_vertical_bar = VerticalProgressBar(
    (
        HORIZONTAL_BAR_X_ORIGIN + 2 * HORIZONTAL_BAR_WIDTH + 20,
        HORIZONTAL_BAR_Y_ORIGIN + VERTICAL_BAR_HEIGHT,
    ),
    (VERTICAL_BAR_WIDTH, VERTICAL_BAR_HEIGHT),
    min_value=0,
    max_value=-VALUES_Y[0],
    direction=VerticalFillDirection.TOP_TO_BOTTOM,
)
main_group.append(bottom_vertical_bar)

delay = 0.5

while True:
    for val in fake__accel_data:
        if val[0] >= 0:
            left_horizontal_bar.value = 0
            right_horizontal_bar.value = val[0]
        if val[0] < 0:
            left_horizontal_bar.value = -val[0]
            right_horizontal_bar.value = 0

        if val[1] >= 0:
            top_vertical_bar.value = val[1]
            bottom_vertical_bar.value = 0
        if val[1] < 0:
            bottom_vertical_bar.value = -val[1]
            top_vertical_bar.value = 0

        display.refresh()
        time.sleep(delay)
