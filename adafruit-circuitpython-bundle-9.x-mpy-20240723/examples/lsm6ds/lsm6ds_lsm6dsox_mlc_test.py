# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT
# LSM6DSOX IMU MLC (Machine Learning Core) Example.
# Download the raw UCF file, copy to storage and reset.

# NOTE: The pre-trained models (UCF files) for the examples can be found here:
# https://github.com/STMicroelectronics/STMems_Machine_Learning_Core/tree/master/application_examples/lsm6dsox

import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX
from adafruit_lsm6ds import Rate, AccelRange, GyroRange

i2c = board.STEMMA_I2C()  # uses board.SCL and board.SDA


# Vibration detection example
UCF_FILE = "lsm6dsox_vibration_monitoring.ucf"
UCF_LABELS = {0: "no vibration", 1: "low vibration", 2: "high vibration"}
# NOTE: Selected data rate and scale must match the MLC data rate and scale.
lsm = LSM6DSOX(i2c, ucf=UCF_FILE)
lsm.gyro_range = GyroRange.RANGE_2000_DPS
lsm.accelerometer_range = AccelRange.RANGE_4G
lsm.accelerometer_data_rate = Rate.RATE_26_HZ
lsm.gyro_data_rate = Rate.RATE_26_HZ


# Head gestures example
# UCF_FILE = "lsm6dsox_head_gestures.ucf"
# UCF_LABELS = {0:"Nod", 1:"Shake", 2:"Stationary", 3:"Swing", 4:"Walk"}
# NOTE: Selected data rate and scale must match the MLC data rate and scale.
# lsm = LSM6DSOX(i2c, ucf=UCF_FILE)
# lsm.gyro_range = GyroRange.RANGE_250_DPS
# lsm.accelerometer_range = AccelRange.RANGE_2G
# lsm.accelerometer_data_rate = Rate.RATE_26_HZ
# lsm.gyro_data_rate = Rate.RATE_26_HZ

# 6 DOF Position example
# UCF_FILE = "lsm6dsox_six_d_position.ucf"
# UCF_LABELS = {0:"None", 1:"X-UP", 2:"X-DOWN", 3:"Y-UP", 4:"Y-DOWN", 5:"Z-UP", 6:"Z-DOWN"}
# NOTE: Selected data rate and scale must match the MLC data rate and scale.
# lsm = LSM6DSOX(i2c, ucf=UCF_FILE)
# lsm.gyro_range = GyroRange.RANGE_250_DPS
# lsm.accelerometer_range = AccelRange.RANGE_2G
# lsm.accelerometer_data_rate = Rate.RATE_26_HZ
# lsm.gyro_data_rate = Rate.RATE_26_HZ


print("MLC configured...")

while True:
    buf = lsm.read_mlc_output()
    if buf is not None:
        print(UCF_LABELS[buf[0]])
        # delay to allow interrupt flag to clear
        # interrupt stays high for one sample interval
        # (38.4 ms @ 26 Hz ot 19.2 ms @ 52Hz)
        time.sleep(0.05)
