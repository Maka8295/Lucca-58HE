# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import busio
from adafruit_atecc.adafruit_atecc import ATECC, _WAKE_CLK_FREQ, CFG_TLS

import adafruit_atecc.adafruit_atecc_cert_util as cert_utils

# -- Enter your configuration below -- #

# Lock the ATECC module when the code is run?
LOCK_ATECC = False
# 2-letter country code
MY_COUNTRY = "US"
# State or Province Name
MY_STATE = "New York"
# City Name
MY_CITY = "New York"
# Organization Name
MY_ORG = "Adafruit"
# Organizational Unit Name
MY_SECTION = "Crypto"
# Which ATECC slot (0-4) to use
ATECC_SLOT = 0
# Generate new private key, or use existing key
GENERATE_PRIVATE_KEY = True

# -- END Configuration, code below -- #

# Initialize the i2c bus
i2c = busio.I2C(board.SCL, board.SDA, frequency=_WAKE_CLK_FREQ)

# Initialize a new atecc object
atecc = ATECC(i2c)

print("ATECC Serial Number: ", atecc.serial_number)

if not atecc.locked:
    if not LOCK_ATECC:
        raise RuntimeError(
            "The ATECC is not locked, set LOCK_ATECC to True in code.py."
        )
    print("Writing default configuration to the device...")
    atecc.write_config(CFG_TLS)
    print("Wrote configuration, locking ATECC module...")
    # Lock ATECC config, data, and otp zones
    atecc.lock_all_zones()
    print("ATECC locked!")

print("Generating Certificate Signing Request...")
# Initialize a certificate signing request with provided info
csr = cert_utils.CSR(
    atecc,
    ATECC_SLOT,
    GENERATE_PRIVATE_KEY,
    MY_COUNTRY,
    MY_STATE,
    MY_CITY,
    MY_ORG,
    MY_SECTION,
)
# Generate CSR
my_csr = csr.generate_csr()
print("-----BEGIN CERTIFICATE REQUEST-----\n")
print(my_csr.decode("utf-8"))
print("-----END CERTIFICATE REQUEST-----")
