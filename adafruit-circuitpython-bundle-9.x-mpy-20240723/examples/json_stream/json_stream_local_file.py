# SPDX-FileCopyrightText: Copyright (c) 2023 Scott Shawcroft for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import sys

import adafruit_json_stream as json_stream

# import json_stream


class FakeResponse:
    def __init__(self, file):
        self.file = file

    def iter_content(self, chunk_size):
        while True:
            yield self.file.read(chunk_size)


f = open(sys.argv[1], "rb")  # pylint: disable=consider-using-with
obj = json_stream.load(FakeResponse(f).iter_content(32))

currently = obj["currently"]
print(currently)
print(currently["time"])
print(currently["icon"])

for i, day in enumerate(obj["daily"]["data"]):
    print(day["time"], day["summary"], day["temperatureHigh"])
    if i > 6:
        break

for source in obj["flags"]["sources"]:
    print(source)
