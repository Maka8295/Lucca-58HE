# SPDX-FileCopyrightText: 2024 Tim Cocks
# SPDX-License-Identifier: MIT
"""
This script can be used to generate a new key pair and output them as JSON.
You can copy the JSON from serial console and paste it into a new file
on the device and then use it with the rsa_json_keys.py example.
"""
import json
import adafruit_rsa


# Create a keypair
print("Generating keypair...")
(public_key, private_key) = adafruit_rsa.newkeys(512)


print("public json:")
print("-------------------------------")
public_obj = {"public_key_arguments": [public_key.n, public_key.e]}
print(json.dumps(public_obj))
print("-------------------------------")


print("private json:")
print("-------------------------------")
private_obj = {
    "private_key_arguments": [
        private_key.n,
        private_key.e,
        private_key.d,
        private_key.p,
        private_key.q,
    ]
}
print(json.dumps(private_obj))
print("-------------------------------")
