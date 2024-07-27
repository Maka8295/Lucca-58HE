# SPDX-FileCopyrightText: 2018 Tony DiCola for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of using the SI4743 RDS FM transmitter.

import time
import board
import digitalio
import adafruit_si4713

# Specify the FM frequency to transmit on in kilohertz.  As the datasheet
# mentions you can only specify 50khz steps!
FREQUENCY_KHZ = 102300  # 102.300mhz

# Initialize I2C bus.
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

# Initialize SI4713.
# si4713 = adafruit_si4713.SI4713(i2c)

# Alternatively you can specify the I2C address of the device if it changed:
# si4713 = adafruit_si4713.SI4713(i2c, address=0x11)

# If you hooked up the reset line you should specify that too.  Make sure
# to pass in a DigitalInOut instance.  You will need the reset pin with the
# Raspberry Pi, and probably other devices:
si_reset = digitalio.DigitalInOut(board.D5)

print("initializing si4713 instance")
si4713 = adafruit_si4713.SI4713(i2c, reset=si_reset, timeout_s=0.5)
print("done")

# Measure the noise level for the transmit frequency (this assumes automatic
# antenna capacitance setting, but see below to adjust to a specific value).
noise = si4713.received_noise_level(FREQUENCY_KHZ)
# Alternatively measure with a specific frequency and antenna capacitance.
# This is not common but you can specify antenna capacitance as a value in pF
# from 0.25 to 47.75 (will use 0.25 steps internally).  If you aren't sure
# about this value, stick with the default automatic capacitance above!
# noise = si4713.received_noise_level(FREQUENCY_KHZ, 0.25)
print("Noise at {0:0.3f} mhz: {1} dBuV".format(FREQUENCY_KHZ / 1000.0, noise))

# Tune to transmit with 115 dBuV power (max) and automatic antenna tuning
# capacitance (default, what you probably want).
si4713.tx_frequency_khz = FREQUENCY_KHZ
si4713.tx_power = 115

# Configure RDS broadcast with program ID 0xADAF (a 16-bit value you specify).
# You can also set the broadcast station name (up to 96 bytes long) and
# broadcast buffer/song information (up to 106 bytes long).  Setting these is
# optional and you can later update them by setting the rds_station and
# rds_buffer property respectively.  Be sure to explicitly specify station
# and buffer as byte strings so the character encoding is clear.
si4713.configure_rds(0xADAF, station=b"AdaRadio", rds_buffer=b"Adafruit g0th Radio!")

# Print out some transmitter state:
print("Transmitting at {0:0.3f} mhz".format(si4713.tx_frequency_khz / 1000.0))
print("Transmitter power: {0} dBuV".format(si4713.tx_power))
print(
    "Transmitter antenna capacitance: {0:0.2} pF".format(si4713.tx_antenna_capacitance)
)

# Set GPIO1 and GPIO2 to actively driven outputs.
si4713.gpio_control(gpio1=True, gpio2=True)

# Main loop will print input audio level and state and blink the GPIOs.
print("Broadcasting...")
while True:
    # Print input audio level and state.
    print("Input level: {0} dBfs".format(si4713.input_level))
    print("ASQ status: 0x{0:02x}".format(si4713.audio_signal_status))
    # 'Blink' GPIO1 and GPIO2 alternatively on and off.
    si4713.gpio_set(gpio1=True, gpio2=False)  # GPIO1 high, GPIO2 low
    time.sleep(0.5)
    si4713.gpio_set(gpio1=False, gpio2=True)  # GPIO1 low, GPIO2 high
    time.sleep(0.5)
