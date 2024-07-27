# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

from adafruit_fakerequests import Fake_Requests

response = Fake_Requests("local.txt")
print(response.text)
