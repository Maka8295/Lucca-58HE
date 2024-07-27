# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import adafruit_jwt

# Get private RSA key from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# Run jwt_simpletest_secrets.py to generate the private key
if "private_key" not in secrets:
    raise KeyError("Run jwt_simpletest_secrets.py to generate the private key!")

# Sample JWT Claims
claims = {"iss": "joe", "exp": 1300819380, "name": "John Doe", "admin": True}

# Generate a JWT
print("Generating JWT...")
encoded_jwt = adafruit_jwt.JWT.generate(claims, secrets["private_key"], algo="RS256")
print("Encoded JWT: ", encoded_jwt)

# Validate a provided JWT
print("Decoding JWT...")
decoded_jwt = adafruit_jwt.JWT.validate(encoded_jwt)
print("JOSE Header: {}\nJWT Claims: {}".format(decoded_jwt[0], decoded_jwt[1]))
