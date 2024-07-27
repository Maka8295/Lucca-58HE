# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Adafruit RSA Tests
"""
import time
import adafruit_rsa


def test_encrypt_decrypt():
    # Generate general purpose keys
    (pub, priv) = adafruit_rsa.newkeys(256, log_level="DEBUG")
    msg = "blinka".encode("utf-8")
    msg_enc = adafruit_rsa.encrypt(msg, pub)
    msg_dec = adafruit_rsa.decrypt(msg_enc, priv)
    assert msg == msg_dec, "Decrypted message does not match original message"


def test_mod_msg():
    """Modifies an enecrypted message, asserts failure"""
    # Generate general purpose keys
    (pub, priv) = adafruit_rsa.newkeys(256, log_level="DEBUG")
    msg = "blinka".encode("utf-8")
    msg_enc = adafruit_rsa.encrypt(msg, pub)
    msg_enc = msg_enc[:-1] + b"X"  # change the last byte
    try:
        msg_dec = adafruit_rsa.decrypt(msg_enc, priv)
        assert msg_dec != msg, "ERROR: Decrypted message matches original"
    except adafruit_rsa.pkcs1.DecryptionError:
        pass


# pylint: disable=unused-variable
def test_randomness():
    """Encrypt msg 2x yields diff. encrypted values."""
    # Generate general purpose keys
    (pub, priv) = adafruit_rsa.newkeys(256, log_level="DEBUG")
    msg = "blinka".encode("utf-8")
    msg_enc_1 = adafruit_rsa.encrypt(msg, pub)
    msg_enc_2 = adafruit_rsa.encrypt(msg, pub)
    assert msg_enc_1 != msg_enc_2, "Messages should yield different values."


def test_sign_verify_sha256():
    """Test SHA256 sign and verify the message."""
    (pub, priv) = adafruit_rsa.newkeys(496, log_level="DEBUG")
    msg = "red apple"
    signature = adafruit_rsa.sign(msg, priv, "SHA-256")
    adafruit_rsa.verify(msg, signature, pub)


def test_sign_verify_sha384():
    """Test SHA-384 sign and verify the message."""
    (pub, priv) = adafruit_rsa.newkeys(624, log_level="DEBUG")
    msg = "red apple"
    signature = adafruit_rsa.sign(msg, priv, "SHA-384")
    adafruit_rsa.verify(msg, signature, pub)


def test_sign_verify_sha512():
    """Test SHA-512 sign and verify the message."""
    (pub, priv) = adafruit_rsa.newkeys(752, log_level="DEBUG")
    msg = "red apple"
    signature = adafruit_rsa.sign(msg, priv, "SHA-512")
    adafruit_rsa.verify(msg, signature, pub)


def test_sign_verify_fail():
    """Check for adafruit_rsa.pkcs1.VerificationError on
    a modified message (invalid signature).
    """
    # Generate general purpose keys
    (pub, priv) = adafruit_rsa.newkeys(256, log_level="DEBUG")
    msg = "red apple"
    signature = adafruit_rsa.sign(msg, priv, "SHA-512")
    msg = "blue apple"
    try:
        adafruit_rsa.verify(msg, signature, pub)
    except adafruit_rsa.pkcs1.VerificationError:
        # Expected error
        pass


# List all tests
all_tests = [
    test_encrypt_decrypt,
    test_mod_msg,
    test_randomness,
    test_sign_verify_sha256,
    test_sign_verify_sha384,
    test_sign_verify_sha512,
]

# Run adafruit_rsa tests
start_time = time.monotonic()
for test_name in all_tests:
    # for i in range(0, len(all_tests)):
    print("Testing: {}".format(test_name))
    test_name()
    print("OK!")
print(
    "Ran {} tests in {} seconds".format(len(all_tests), time.monotonic() - start_time)
)
