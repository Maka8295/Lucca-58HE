# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import adafruit_rsa

# Generate a keypair
#
# Supported Hash method   Suggested minimum key size (bits)
# SHA-256                 496
# SHA-384                 624
# SHA-512                 752
#
(public_key, private_key) = adafruit_rsa.newkeys(496)

# Create a new secret message
message = "Meet me at 6pm"

# Hash the message using SHA-224
hash_method = "SHA-256"
signature = adafruit_rsa.sign(message, private_key, hash_method)

# Verify Message Signature
if adafruit_rsa.verify(message, signature, public_key) != hash_method:
    raise ValueError(
        "Verification failed - signature does not match secret message sent!"
    )
