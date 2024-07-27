# SPDX-FileCopyrightText: Gabriele Pongelli 2021 for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
import board
from adafruit_ina260 import INA260, Mode, ConversionTime


if __name__ == "__main__":
    try:
        i2c = board.I2C()  # uses board.SCL and board.SDA
        # i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector
        ina260 = INA260(i2c)
    except RuntimeError as r_e:
        # catch exception on init, no INA260 chip found
        print(r_e)
        raise r_e

    # set overcurrent limit flag and threshold value
    # 0x0008 x 1,25 mA = 10 mA as alert limit
    ina260.alert_limit = 0x0008

    # alert pin is asserted, can be check with gpiozero
    ina260.overcurrent_limit = True

    # keep the flag high until MASK_ENABLE register will be read
    ina260.alert_latch_enable = True

    ina260.mode = Mode.CONTINUOUS

    # set higher conversion time and wait its value before each read
    ina260.current_conversion_time = ConversionTime.TIME_8_244_ms
    for _ in enumerate(range(5)):
        time.sleep(ConversionTime.get_seconds(ina260.current_conversion_time))
        print(
            f"Current: {ina260.current:.2f} mA, "
            f"Voltage: {ina260.voltage:.2f} V, "
            f"Power: {ina260.power:.2f} mW"
        )

    # supposing meanwhile the alert limit was exceeded, setting an higher limit
    # and clear the ALERT
    # 0x0100 x 1,25 mA = 320 mA as alert limit
    ina260.alert_limit = 0x0100

    # alert function flag bit should be true if alert threshold was exceeded
    print("Alert function flag: ", ina260.alert_function_flag)

    # in latch mode, reading the register clears the ALERT & alert function flag
    print("MASK register:", ina260.mask_enable)

    # reset the whole chip and wait 2 sec
    ina260.reset_bit = True
    time.sleep(2)
    print("MASK_REGISTER check, must be 0x0000 after reset:", ina260.mask_enable)
