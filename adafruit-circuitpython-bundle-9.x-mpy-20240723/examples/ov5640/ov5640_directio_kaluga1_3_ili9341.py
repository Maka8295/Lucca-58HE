# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""
The Kaluga development kit comes in two versions (v1.2 and v1.3); this demo is
tested on v1.3.

The audio board must be mounted between the Kaluga and the LCD, it provides the
I2C pull-ups(!)

The v1.3 development kit's LCD can have one of two chips, the ili9341 or
st7789.  Furthermore, there are at least 2 ILI9341 variants, which differ
by rotation.  This example is written for one if the ILI9341 variants,
the one which usually uses rotation=90 to get a landscape display.
"""

import struct

import board
import busio
import digitalio
import displayio
from adafruit_ticks import ticks_ms, ticks_less
import adafruit_ov5640

# Set to True to enable the various effects & exposure modes to be tested
test_effects = False

# Release any resources currently in use for the displays
displayio.release_displays()

state = digitalio.DigitalInOut(board.IO4)
state.switch_to_output(True)

spi = busio.SPI(MOSI=board.LCD_MOSI, clock=board.LCD_CLK)
display_bus = displayio.FourWire(
    spi,
    command=board.LCD_D_C,
    chip_select=board.LCD_CS,
    reset=board.LCD_RST,
    baudrate=80_000_000,
)
_INIT_SEQUENCE = (
    b"\x01\x80\x80"  # Software reset then delay 0x80 (128ms)
    b"\xEF\x03\x03\x80\x02"
    b"\xCF\x03\x00\xC1\x30"
    b"\xED\x04\x64\x03\x12\x81"
    b"\xE8\x03\x85\x00\x78"
    b"\xCB\x05\x39\x2C\x00\x34\x02"
    b"\xF7\x01\x20"
    b"\xEA\x02\x00\x00"
    b"\xc0\x01\x23"  # Power control VRH[5:0]
    b"\xc1\x01\x10"  # Power control SAP[2:0];BT[3:0]
    b"\xc5\x02\x3e\x28"  # VCM control
    b"\xc7\x01\x86"  # VCM control2
    b"\x36\x01\x40"  # Memory Access Control
    b"\x37\x01\x00"  # Vertical scroll zero
    b"\x3a\x01\x55"  # COLMOD: Pixel Format Set
    b"\xb1\x02\x00\x18"  # Frame Rate Control (In Normal Mode/Full Colors)
    b"\xb6\x03\x08\x82\x27"  # Display Function Control
    b"\xF2\x01\x00"  # 3Gamma Function Disable
    b"\x26\x01\x01"  # Gamma curve selected
    b"\xe0\x0f\x0F\x31\x2B\x0C\x0E\x08\x4E\xF1\x37\x07\x10\x03\x0E\x09\x00"  # Set Gamma
    b"\xe1\x0f\x00\x0E\x14\x03\x11\x07\x31\xC1\x48\x08\x0F\x0C\x31\x36\x0F"  # Set Gamma
    b"\x11\x80\x78"  # Exit Sleep then delay 0x78 (120ms)
    b"\x29\x80\x78"  # Display on then delay 0x78 (120ms)
)

display = displayio.Display(display_bus, _INIT_SEQUENCE, width=320, height=240)

bus = busio.I2C(scl=board.CAMERA_SIOC, sda=board.CAMERA_SIOD)
cam = adafruit_ov5640.OV5640(
    bus,
    data_pins=board.CAMERA_DATA,
    clock=board.CAMERA_PCLK,
    vsync=board.CAMERA_VSYNC,
    href=board.CAMERA_HREF,
    mclk=board.CAMERA_XCLK,
    size=adafruit_ov5640.OV5640_SIZE_QVGA,
)

cam.flip_x = False
cam.flip_y = False
chip_id = cam.chip_id
print(f"Detected 0x{chip_id:x}")
cam.test_pattern = False
cam.effect = adafruit_ov5640.OV5640_SPECIAL_EFFECT_NONE
cam.saturation = 3
bitmap = displayio.Bitmap(cam.width, cam.height, 65536)
print(len(memoryview(bitmap)))
display.auto_refresh = False


def special_modes(cam_obj):
    def effect_modes(cam_obj):
        for i in [
            "NONE",
            "NEGATIVE",
            "GRAYSCALE",
            "RED_TINT",
            "GREEN_TINT",
            "BLUE_TINT",
            "SEPIA",
        ]:
            print(f"Effect {i}")
            cam_obj.effect = getattr(adafruit_ov5640, f"OV5640_SPECIAL_EFFECT_{i}")
            yield
        cam_obj.effect = adafruit_ov5640.OV5640_SPECIAL_EFFECT_NONE

    def saturation_modes(cam_obj):
        for i in range(-4, 5):
            print(f"Saturation {i}")
            cam_obj.saturation = i
            yield
        cam_obj.saturation = 0

    def brightness_modes(cam_obj):
        for i in range(-4, 5):
            print(f"Brightness {i}")
            cam_obj.brightness = i
            yield
        cam_obj.brightness = 0

    def contrast_modes(cam_obj):
        for i in range(-3, 4):
            print(f"Contrast {i}")
            cam_obj.contrast = i
            yield
        cam_obj.contrast = 0

    def white_balance_modes(cam_obj):  # pylint: disable=unused-variable
        for i in ["AUTO", "SUNNY", "FLUORESCENT", "CLOUDY", "INCANDESCENT"]:
            print(f"White Balance {i}")
            cam_obj.white_balance = getattr(
                adafruit_ov5640, f"OV5640_WHITE_BALANCE_{i}"
            )
            yield
        cam_obj.white_balance = adafruit_ov5640.OV5640_WHITE_BALANCE_AUTO

    def exposure_value_modes(cam_obj):  # pylint: disable=unused-variable
        for i in range(-3, 4):
            print(f"EV {i}")
            cam_obj.exposure_value = i
            yield
        cam_obj.exposure_value = 0

    def nite_modes(cam_obj):  # pylint: disable=unused-variable
        print("Night Mode On")
        cam_obj.night_mode = True
        print(cam_obj.night_mode)
        yield
        print("Night Mode Off")
        cam_obj.night_mode = False
        print(cam_obj.night_mode)
        yield

    def test_modes(cam_obj):
        print("Test pattern On")
        cam_obj.test_pattern = True
        yield
        print("Test pattern Off")
        cam_obj.test_pattern = False
        yield

    while True:
        yield from test_modes(cam_obj)
        yield from contrast_modes(cam_obj)
        yield from effect_modes(cam_obj)
        yield from saturation_modes(cam_obj)
        yield from brightness_modes(cam_obj)
        # These don't work right (yet)
        # yield from exposure_value_modes(cam_obj)  # Issue #8
        # yield from nite_modes(cam_obj) # Issue #6


def main():
    deadline = 0
    effects = iter((None,))

    display.auto_refresh = False
    display_bus.send(42, struct.pack(">hh", 0, bitmap.width - 1))
    display_bus.send(43, struct.pack(">hh", 0, bitmap.height - 1))

    if test_effects:
        time_per_effect = 1500
        deadline = ticks_ms() + time_per_effect
        effects = special_modes(cam)

    while True:
        if test_effects:
            now = ticks_ms()
            if ticks_less(deadline, now):
                deadline += time_per_effect
                next(effects)
        state.value = True
        cam.capture(bitmap)
        state.value = False
        display_bus.send(44, bitmap)


main()
