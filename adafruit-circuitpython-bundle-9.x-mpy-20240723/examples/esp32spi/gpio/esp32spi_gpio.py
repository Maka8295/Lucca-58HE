# SPDX-FileCopyrightText: 2019 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
import random
import board
from digitalio import DigitalInOut, Direction
import pulseio
from adafruit_esp32spi import adafruit_esp32spi


# ESP32SPI Digital and Analog Pin Reads & Writes

# This example targets a Feather M4 or ItsyBitsy M4 as the CircuitPython MCU,
# along with either an ESP32 Feather or ESP32 Breakout as Wi-Fi co-processor.
# You may need to choose different pins for other targets.


def esp_reset_all():
    # esp.reset() will reset the ESP32 using its RST pin
    # side effect is re-initializing ESP32 pin modes and debug output
    esp.reset()
    time.sleep(1)
    # (re-)set NINA serial debug on ESP32 TX
    esp.set_esp_debug(True)  # False, True
    # (re-)set digital pin modes
    esp_init_pin_modes(ESP_D_R_PIN, ESP_D_W_PIN)


def esp_init_pin_modes(din, dout):
    # ESP32 Digital Input
    esp.set_pin_mode(din, 0x0)

    # ESP32 Digital Output (no output on pins 34-39)
    esp.set_pin_mode(dout, 0x1)


# M4 R/W Pin Assignments
M4_D_W_PIN = DigitalInOut(board.A1)  # digital write to ESP_D_R_PIN
M4_D_W_PIN.direction = Direction.OUTPUT
M4_A_R_PIN = pulseio.PulseIn(board.A0, maxlen=64)  # PWM read from ESP_A_W_PIN
M4_A_R_PIN.pause()

# ESP32 R/W Pin assignments & connections
ESP_D_R_PIN = 12  # digital read from M4_D_W_PIN
ESP_D_W_PIN = 13  # digital write to Red LED on Feather ESP32 and ESP32 Breakout
# ESP32 Analog Input using ADC1
# esp.set_pin_mode(36, 0x0)  # Hall Effect Sensor
# esp.set_pin_mode(37, 0x0)  # Not Exposed
# esp.set_pin_mode(38, 0x0)  # Not Exposed
# esp.set_pin_mode(39, 0x0)  # Hall Effect Sensor
# esp.set_pin_mode(32, 0x0)  # INPUT OK
# esp.set_pin_mode(33, 0x0)  # DO NOT USE: ESP32SPI Busy/!Rdy
# esp.set_pin_mode(34, 0x0)  # INPUT OK
# esp.set_pin_mode(35, 0x0)  # INPUT OK (1/2 of Battery on ESP32 Feather)
ESP_A_R_PIN = 32  # analog read from 10k potentiometer
# ESP32 Analog (PWM/LEDC) Output (no output on pins 34-39)
ESP_A_W_PIN = 27  # analog (PWM) write to M4_A_R_PIN

spi = board.SPI()
# Airlift FeatherWing & Bitsy Add-On compatible
esp32_cs = DigitalInOut(board.D13)  # M4 Red LED
esp32_ready = DigitalInOut(board.D11)
esp32_reset = DigitalInOut(board.D12)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

esp_reset_all()

print("ESP32 Firmware:", esp.firmware_version)

print(
    "ESP32 MAC:      {5:02X}:{4:02X}:{3:02X}:{2:02X}:{1:02X}:{0:02X}".format(
        *esp.MAC_address
    )
)

# initial digital write values
m4_d_w_val = False
esp_d_w_val = False

while True:
    print("\nESP32 DIGITAL:")

    # ESP32 digital read
    try:
        M4_D_W_PIN.value = m4_d_w_val
        print("M4 wrote:", m4_d_w_val, end=" ")
        # b/c ESP32 might have reset out from under us
        esp_init_pin_modes(ESP_D_R_PIN, ESP_D_W_PIN)
        esp_d_r_val = esp.set_digital_read(ESP_D_R_PIN)
        print("--> ESP read:", esp_d_r_val)
    except OSError as e:
        print("ESP32 Error", e)
        esp_reset_all()

    # ESP32 digital write
    try:
        # b/c ESP32 might have reset out from under us
        esp_init_pin_modes(ESP_D_R_PIN, ESP_D_W_PIN)
        esp.set_digital_write(ESP_D_W_PIN, esp_d_w_val)
        print("ESP wrote:", esp_d_w_val, "--> Red LED")
    except OSError as e:
        print("ESP32 Error", e)
        esp_reset_all()

    print("ESP32 ANALOG:")

    # ESP32 analog read
    try:
        esp_a_r_val = esp.set_analog_read(ESP_A_R_PIN)
        print(
            "Potentiometer --> ESP read: ",
            esp_a_r_val,
            " (",
            "{:1.1f}".format(esp_a_r_val * 3.3 / 65536),
            "v)",
            sep="",
        )
    except OSError as e:
        print("ESP32 Error", e)
        esp_reset_all()

    # ESP32 analog write
    try:
        # don't set the low end to 0 or the M4's pulseio read will stall
        esp_a_w_val = random.uniform(0.1, 0.9)
        esp.set_analog_write(ESP_A_W_PIN, esp_a_w_val)
        print(
            "ESP wrote: ",
            "{:1.2f}".format(esp_a_w_val),
            " (",
            "{:d}".format(int(esp_a_w_val * 65536)),
            ")",
            " (",
            "{:1.1f}".format(esp_a_w_val * 3.3),
            "v)",
            sep="",
            end=" ",
        )

        # ESP32 "analog" write is a 1000Hz PWM
        # use pulseio to extract the duty cycle
        M4_A_R_PIN.clear()
        M4_A_R_PIN.resume()
        while len(M4_A_R_PIN) < 2:
            pass
        M4_A_R_PIN.pause()
        duty = M4_A_R_PIN[0] / (M4_A_R_PIN[0] + M4_A_R_PIN[1])
        print(
            "--> M4 read: ",
            "{:1.2f}".format(duty),
            " (",
            "{:d}".format(int(duty * 65536)),
            ")",
            " (",
            "{:1.1f}".format(duty * 3.3),
            "v)",
            " [len=",
            len(M4_A_R_PIN),
            "]",
            sep="",
        )

    except OSError as e:
        print("ESP32 Error", e)
        esp_reset_all()

    # toggle digital write values
    m4_d_w_val = not m4_d_w_val
    esp_d_w_val = not esp_d_w_val

    time.sleep(5)
