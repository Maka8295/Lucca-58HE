# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example will show the current temperature in the Serial Console
whenever the FeatherWing senses that it has been tapped
"""

import time
from adafruit_featherwing import tempmotion_featherwing

temp_motion = tempmotion_featherwing.TempMotionFeatherWing()
temp_motion.enable_tap_detection()
while True:
    if temp_motion.events["tap"]:
        print("The temperature is %f" % temp_motion.temperature)
    time.sleep(1)
