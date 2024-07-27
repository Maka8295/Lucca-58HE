# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Crickit library demo - Continuous servo

from adafruit_crickit import crickit

# Start spinning continuous servo on Servo 1 terminal backwards at half speed.
crickit.continuous_servo_1.throttle = -0.5
