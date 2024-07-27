# SPDX-FileCopyrightText: Copyright (c) 2021 Rose Hooper for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import adafruit_pixelbuf


class TestBuf(adafruit_pixelbuf.PixelBuf):
    called = False

    @property
    def n(self):
        return len(self)

    def _transmit(self, buffer):  # pylint: disable=unused-argument
        self.called = True


buf = TestBuf(20, "RGBW", brightness=0.5, auto_write=True)
buf[0] = (1, 2, 3)
buf[1] = (1, 2, 3, 4)
buf[2] = (2, 2, 2)

print(buf[0])
print(buf[0:2])
print(buf[0:2:2])
print(buf.called)
