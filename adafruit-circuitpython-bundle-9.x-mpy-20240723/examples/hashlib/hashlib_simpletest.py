# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# pylint: disable=no-member, line-too-long
import adafruit_hashlib as hashlib

# Bytes-to-encode
byte_string = b"CircuitPython"

# Create an MD5 message
print("--MD5--")
m = hashlib.md5()
# Update the hash object with byte_string
m.update(byte_string)
# Obtain the digest, digest size, and block size
print(
    "Msg Digest: {}\nMsg Digest Size: {}\nMsg Block Size: {}".format(
        m.hexdigest(), m.digest_size, m.block_size
    )
)
# Validate the digest against CPython3 hashlib-md5
assert (
    m.hexdigest() == "6a61334a5d9f848bea9affcd82864819"
), "Digest does not match expected string."

# Create a SHA-1 message
print("--SHA1--")
m = hashlib.sha1()
# Update the hash object with byte_string
m.update(byte_string)
# Obtain the digest, digest size, and block size
print(
    "Msg Digest: {}\nMsg Digest Size: {}\nMsg Block Size: {}".format(
        m.hexdigest(), m.digest_size, m.block_size
    )
)
# Validate the digest against CPython3 hashlib-sha1
assert (
    m.hexdigest() == "62c6e222ccd72f21b8ce0c61f42860d6c70954c0"
), "Digest does not match expected string."


# Create a SHA-224 message
print("--SHA224--")
m = hashlib.sha224()
# Update the hash object with byte_string
m.update(byte_string)
# Obtain the digest, digest size, and block size
print(
    "Msg Digest: {}\nMsg Digest Size: {}\nMsg Block Size: {}".format(
        m.hexdigest(), m.digest_size, m.block_size
    )
)
# Validate the digest against CPython hashlib-sha224
assert (
    m.hexdigest() == "744535a10879be6b18bbcdd135032891346f530a7845d580f7869f36"
), "Digest does not match expected string."

# SHA-256
print("--SHA256--")
m = hashlib.sha256()
# Update the hash object with byte_string
m.update(byte_string)
# Obtain the digest, digest size, and block size
print(
    "Msg Digest: {}\nMsg Digest Size: {}\nMsg Block Size: {}".format(
        m.hexdigest(), m.digest_size, m.block_size
    )
)
# Validate the digest against CPython hashlib-sha256
assert (
    m.hexdigest() == "3ce8334ca39e66afb9c37d571da4caad68ab4a8bcbd6d584f75e4268e36c0954"
), "Digest does not match expected string."

# SHA-384
print("--SHA384--")
m = hashlib.sha384()
# Update the hash object with byte_string
m.update(byte_string)
# Obtain the digest, digest size, and block size
print(
    "Msg Digest: {}\nMsg Digest Size: {}\nMsg Block Size: {}".format(
        m.hexdigest(), m.digest_size, m.block_size
    )
)
# Validate the digest against CPython hashlib-sha384
assert (
    m.hexdigest()
    == "7a12f0815f5511b8ba52c67922d1ae86dfd9bfcc4e0799ad89a9f01fc526c8f074ddb5948c06db9893536f2e65c7621b"
), "Digest does not match expected string."

# SHA-512
print("--SHA512--")
m = hashlib.sha512()
# Update the hash object with byte_string
m.update(byte_string)
# Obtain the digest, digest size, and block size
print(
    "Msg Digest: {}\nMsg Digest Size: {}\nMsg Block Size: {}".format(
        m.hexdigest(), m.digest_size, m.block_size
    )
)
# Validate the digest against CPython hashlib-sha512
assert (
    m.hexdigest()
    == "20a88a9b04aa490e457f8980e57331bc85c4d6ca30735a9e502f817e74011a9ece07078e53adf70c232ac91f6c79d4cd6cc69426cd77535645fe9016a71122c2"
), "Digest does not match expected string."
