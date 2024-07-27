# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import board
import busio
from digitalio import DigitalInOut
import adafruit_bno08x
from adafruit_bno08x.i2c import BNO08X_I2C

i2c = busio.I2C(board.SCL, board.SDA)
reset_pin = DigitalInOut(board.D5)
bno = BNO08X_I2C(i2c, reset=reset_pin, debug=False)

bno.begin_calibration()
# TODO: UPDATE UART/SPI
bno.enable_feature(adafruit_bno08x.BNO_REPORT_MAGNETOMETER)
bno.enable_feature(adafruit_bno08x.BNO_REPORT_GAME_ROTATION_VECTOR)
start_time = time.monotonic()
calibration_good_at = None
while True:
    time.sleep(0.1)

    print("Magnetometer:")
    mag_x, mag_y, mag_z = bno.magnetic  # pylint:disable=no-member
    print("X: %0.6f  Y: %0.6f Z: %0.6f uT" % (mag_x, mag_y, mag_z))
    print("")

    print("Game Rotation Vector Quaternion:")
    (
        game_quat_i,
        game_quat_j,
        game_quat_k,
        game_quat_real,
    ) = bno.game_quaternion  # pylint:disable=no-member
    print(
        "I: %0.6f  J: %0.6f K: %0.6f  Real: %0.6f"
        % (game_quat_i, game_quat_j, game_quat_k, game_quat_real)
    )
    calibration_status = bno.calibration_status
    print(
        "Magnetometer Calibration quality:",
        adafruit_bno08x.REPORT_ACCURACY_STATUS[calibration_status],
        " (%d)" % calibration_status,
    )
    if not calibration_good_at and calibration_status >= 2:
        calibration_good_at = time.monotonic()
    if calibration_good_at and (time.monotonic() - calibration_good_at > 5.0):
        input_str = input("\n\nEnter S to save or anything else to continue: ")
        if input_str.strip().lower() == "s":
            bno.save_calibration_data()
            break
        calibration_good_at = None
    print("**************************************************************")

print("calibration done")
