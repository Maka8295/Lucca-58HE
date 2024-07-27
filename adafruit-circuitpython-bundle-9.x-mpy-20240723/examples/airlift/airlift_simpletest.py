# SPDX-FileCopyrightText: 2020 Dan Halbert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

# Test works for boards with onboard adapters.

import _bleio
from adafruit_airlift.esp32 import ESP32

esp32 = ESP32()
adapter = esp32.start_bluetooth()
_bleio.set_adapter(adapter)  # pylint: disable=no-member

print(_bleio.adapter.address)
