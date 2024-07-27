# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""
Take a 10-frame stop motion GIF image.

This example requires:
 * `Espressif Kaluga v1.3 <https://www.adafruit.com/product/4729>`_ with compatible LCD display
 * `MicroSD card breakout board + <https://www.adafruit.com/product/254>`_ connected as follows:
    * CLK to board.IO18
    * DI to board.IO14
    * DO to board.IO17
    * CS to IO12
    * GND to GND
    * 5V to 5V
 * A compatible SD card inserted in the SD card slot
 * A compatible OV5640 camera module connected to the camera header

To use:

Insert an SD card and power on.

Set up the first frame using the viewfinder. Click the REC button to take a frame.

Set up the next frame using the viewfinder. The previous and current frames are
blended together on the display, which is called an "onionskin".  Click the REC
button to take the next frame.

After 10 frames are recorded, the GIF is complete and you can begin recording another.


About the Kaluga development kit:

The Kaluga development kit comes in two versions (v1.2 and v1.3); this demo is
tested on v1.3.

The audio board must be mounted between the Kaluga and the LCD, it provides the
I2C pull-ups(!)

The v1.3 development kit's LCD can have one of two chips, the ili9341 or
st7789.  Furthermore, there are at least 2 ILI9341 variants, which differ
by rotation.  This example is written for one if the ILI9341 variants,
the one which usually uses rotation=90 to get a landscape display.
"""

import os
import struct

import analogio
import bitmaptools
import board
import busio
import displayio
import gifio
import sdcardio
import storage

import adafruit_ov5640

V_RECORD = int(2.41 * 65536 / 3.3)
V_FUZZ = 2000

a = analogio.AnalogIn(board.IO6)


def record_pressed():
    value = a.value
    return abs(value - V_RECORD) < V_FUZZ


displayio.release_displays()
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

sd_spi = busio.SPI(clock=board.IO18, MOSI=board.IO14, MISO=board.IO17)
sd_cs = board.IO12
sdcard = sdcardio.SDCard(sd_spi, sd_cs, baudrate=24_000_000)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

bus = busio.I2C(scl=board.CAMERA_SIOC, sda=board.CAMERA_SIOD)
cam = adafruit_ov5640.OV5640(
    bus,
    data_pins=board.CAMERA_DATA,
    clock=board.CAMERA_PCLK,
    vsync=board.CAMERA_VSYNC,
    href=board.CAMERA_HREF,
    mclk=board.CAMERA_XCLK,
    size=adafruit_ov5640.OV5640_SIZE_240X240,
)


def exists(filename):
    try:
        os.stat(filename)
        return True
    except OSError as _:
        return False


_image_counter = 0


def next_filename(extension="jpg"):
    global _image_counter  # pylint: disable=global-statement
    while True:
        filename = f"/sd/img{_image_counter:04d}.{extension}"
        if exists(filename):
            print(f"File exists: {filename}", end="\r")
            _image_counter += 1
            continue
        print()
        return filename


# Pre-cache the next image number
next_filename("gif")

# Blank the whole display, we'll draw what we want with directio
empty_group = displayio.Group()
display.root_group = empty_group
display.auto_refresh = False
display.refresh()


def open_next_image(extension="jpg"):
    while True:
        filename = next_filename(extension)
        print("# writing to", filename)
        return open(filename, "wb")


cam.flip_x = False
cam.flip_y = False
chip_id = cam.chip_id
print(f"Detected 0x{chip_id:x}")
cam.test_pattern = False
cam.effect = adafruit_ov5640.OV5640_SPECIAL_EFFECT_NONE
cam.saturation = 3

# Alternately recording to these two bitmaps
rec1 = displayio.Bitmap(cam.width, cam.height, 65536)
rec2 = displayio.Bitmap(cam.width, cam.height, 65536)
# Prior frame kept here
old_frame = displayio.Bitmap(cam.width, cam.height, 65536)
# Displayed (onion skinned) frame here
onionskin = displayio.Bitmap(cam.width, cam.height, 65536)

ow = (display.width - onionskin.width) // 2
oh = (display.height - onionskin.height) // 2
display_bus.send(42, struct.pack(">hh", ow, onionskin.width + ow - 1))
display_bus.send(43, struct.pack(">hh", oh, onionskin.height + ow - 1))


class ContinuousCapture:
    def __init__(self, camera, buffer1, buffer2):
        camera = getattr(camera, "_imagecapture", camera)
        self._camera = camera
        print("buffer1", buffer1)
        print("buffer2", buffer2)
        camera.continuous_capture_start(buffer1, buffer2)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._camera.continuous_capture_stop()

    def __enter__(self):
        return self

    def get_frame(self):
        return self._camera.continuous_capture_get_frame()

    __next__ = get_frame


def wait_record_pressed_update_display(first_frame, cap):
    while record_pressed():
        pass
    while True:
        frame = cap.get_frame()
        if record_pressed():
            return frame

        if first_frame:
            # First frame -- display as-is
            display_bus.send(44, frame)
        else:
            bitmaptools.alphablend(
                onionskin, old_frame, frame, displayio.Colorspace.RGB565_SWAPPED
            )
            display_bus.send(44, onionskin)


def take_stop_motion_gif(n_frames=10, replay_frame_time=0.3):
    print(f"0/{n_frames}")
    with ContinuousCapture(cam, rec1, rec2) as cap:
        frame = wait_record_pressed_update_display(True, cap)
        with open_next_image("gif") as f, gifio.GifWriter(
            f, cam.width, cam.height, displayio.Colorspace.RGB565_SWAPPED, dither=True
        ) as g:
            g.add_frame(frame, replay_frame_time)
            for i in range(1, n_frames):
                print(f"{i}/{n_frames}")

                # CircuitPython Versions <= 8.2.0
                if hasattr(old_frame, "blit"):
                    old_frame.blit(
                        0, 0, frame, x1=0, y1=0, x2=frame.width, y2=frame.height
                    )

                # CircuitPython Versions >= 9.0.0
                else:
                    bitmaptools.blit(
                        old_frame,
                        frame,
                        0,
                        0,
                        x1=0,
                        y1=0,
                        x2=frame.width,
                        y2=frame.height,
                    )

                frame = wait_record_pressed_update_display(False, cap)
                g.add_frame(frame, replay_frame_time)
            print("done")


est_frame_size = cam.width * cam.height * 128 // 126 + 1
est_hdr_size = 1000

dither = True
while True:
    take_stop_motion_gif()
