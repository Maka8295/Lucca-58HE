# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""
The Kaluga development kit comes in two versions (v1.2 and v1.3); this demo is
tested on v1.3.

The audio board must be mounted between the Kaluga and the LCD, it provides the
I2C pull-ups(!)

You also need to place ov5640_jpeg_kaluga1_3_boot.py at CIRCUITPY/boot.py.
Then, hold the Mode button (button K2 on the audio board) while resetting the
board to make the internal flash readable by CircuitPython.
"""

import time

import board
import busio
import displayio
import microcontroller

import adafruit_ili9341
import adafruit_ov5640

# Release any resources currently in use for the displays
displayio.release_displays()
spi = busio.SPI(MOSI=board.LCD_MOSI, clock=board.LCD_CLK)
display_bus = displayio.FourWire(
    spi,
    command=board.LCD_D_C,
    chip_select=board.LCD_CS,
    reset=board.LCD_RST,
    baudrate=80_000_000,
)
display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240, rotation=90)

try:
    with open("/boot_out.txt", "ab") as f:
        pass
except OSError as e:
    print(e)
    print(
        "A 'read-only filesystem' error occurs if you did not correctly install"
        "\nov5640_jpeg_kaluga1_3_boot.py as CIRCUITPY/boot.py and reset the"
        '\nboard while holding the "mode" button'
        "\n\nThis message is also shown after the board takes a picture and auto-restarts"
    )
    raise SystemExit from e

bus = busio.I2C(scl=board.CAMERA_SIOC, sda=board.CAMERA_SIOD)
cam = adafruit_ov5640.OV5640(
    bus,
    data_pins=board.CAMERA_DATA,
    clock=board.CAMERA_PCLK,
    vsync=board.CAMERA_VSYNC,
    href=board.CAMERA_HREF,
    mclk=board.CAMERA_XCLK,
    size=adafruit_ov5640.OV5640_SIZE_QSXGA,
)

cam.colorspace = adafruit_ov5640.OV5640_COLOR_JPEG
cam.quality = 5
b = bytearray(cam.capture_buffer_size)
print(f"Capturing jpeg image of up to {len(b)} bytes")
jpeg = cam.capture(b)

print(f"Captured {len(jpeg)} bytes of jpeg data")
try:
    print(end="Writing to internal storage (this is SLOW)")
    with open("/cam.jpg", "wb") as f:
        for i in range(0, len(jpeg), 4096):
            print(end=".")
            f.write(jpeg[i : i + 4096])
    print()
    print("Wrote to CIRCUITPY/cam.jpg")
    print("Resetting so computer sees new content of CIRCUITPY")
    time.sleep(0.5)
    microcontroller.reset()  # pylint: disable=no-member

except OSError as e:
    print(e)
    print(
        "A 'read-only filesystem' error occurs if you did not correctly install"
        "\nov5640_jpeg_kaluga1_3_boot.py as CIRCUITPY/boot.py and reset the board"
    )
