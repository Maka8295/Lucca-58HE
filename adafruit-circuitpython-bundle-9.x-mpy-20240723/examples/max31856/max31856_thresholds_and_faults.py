# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import digitalio
import adafruit_max31856

# Create sensor object, communicating over the board's default SPI bus
spi = board.SPI()

# allocate a CS pin and set the direction
cs = digitalio.DigitalInOut(board.D0)
cs.direction = digitalio.Direction.OUTPUT

# create a thermocouple object with the above
thermocouple = adafruit_max31856.MAX31856(spi, cs)

# set the temperature thresholds for the thermocouple and cold junction
thermocouple.temperature_thresholds = (-1.5, 30.8)
thermocouple.reference_temperature_thresholds = (-1.0, 30.5)
current_faults = {}
current_cj_thresholds = (0, 0)
current_temp_thresholds = (0, 0)
print(thermocouple.reference_temperature_thresholds)
while True:
    current_temp_thresholds = thermocouple.temperature_thresholds
    current_cj_thresholds = thermocouple.reference_temperature_thresholds
    current_faults = thermocouple.fault
    print(
        "Temps:    %.2f :: cj: %.2f"
        % (thermocouple.temperature, thermocouple.reference_temperature)
    )
    print("Thresholds:")
    print("Temp low: %.2f high: %.2f" % current_temp_thresholds)
    print("CJ low:   %.2f high: %.2f" % current_cj_thresholds)
    print("")
    print("Faults:")
    print(
        "Temp Hi:    %s | CJ Hi:    %s"
        % (current_faults["tc_high"], current_faults["cj_high"])
    )
    print(
        "Temp Low:   %s | CJ Low:   %s"
        % (current_faults["tc_low"], current_faults["cj_low"])
    )
    print(
        "Temp Range: %s | CJ Range: %s"
        % (current_faults["tc_range"], current_faults["cj_range"])
    )
    print("")
    print(
        "Open Circuit: %s Voltage Over/Under: %s"
        % (current_faults["open_tc"], current_faults["voltage"])
    )
    print("")

    time.sleep(1.0)
