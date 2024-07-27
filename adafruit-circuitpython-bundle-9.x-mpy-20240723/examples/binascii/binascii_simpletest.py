# SPDX-FileCopyrightText: 2020 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

from adafruit_binascii import hexlify, unhexlify, a2b_base64, b2a_base64

print("-- Binary<->Hex Conversions --")
# Binary data.
data = b"CircuitPython is Awesome!"
print("Original Binary Data: ", data)

# Get the hexadecimal representation of the binary data
hex_data = hexlify(data)
print("Hex Data: ", hex_data)
# Verify data
assert (
    hex_data == b"43697263756974507974686f6e20697320417765736f6d6521"
), "hexlified data does not match expected data."
# Get the binary data represented by hex_data
bin_data = unhexlify(hex_data)
print("Binary Data: ", bin_data)
# Verify data
assert bin_data == data, "unhexlified binary data does not match original binary data."

print("-- Base64 ASCII <-> Binary Conversions --")
data = b"Blinka"
print("Original Binary Data: ", data)
# Convert binary data to a line of ASCII characters in base64 coding.
b64_ascii_data = b2a_base64(data)
print("Base64 ASCII Data: ", b64_ascii_data)
assert b64_ascii_data == b"Qmxpbmth\n", "Expected base64 coding does not match."

# Convert a block of base64 data back to binary data.
bin_data = a2b_base64(b"Qmxpbmth\n")
print("Converted b64 ASCII->Binary Data: ", bin_data)
assert bin_data == data, "Expected binary data does not match."
