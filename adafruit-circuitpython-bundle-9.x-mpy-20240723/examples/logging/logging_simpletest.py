# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# pylint:disable=undefined-variable,wildcard-import,no-name-in-module
# pylint:disable=no-member,invalid-name

"""Briefly exercise the logger and null logger."""

import adafruit_logging as logging

# This should produce an info output via default handler.

logger_default_handler = logging.getLogger("default_handler")
logger_default_handler.setLevel(logging.INFO)
logger_default_handler.info("Default handler: Info message")
assert not logger_default_handler.hasHandlers()

# This should produce an error output via Stream Handler.

logger = logging.getLogger("test")
print_handler = logging.StreamHandler()
logger.addHandler(print_handler)
assert logger.hasHandlers()

logger.setLevel(logging.ERROR)
logger.info("Stream Handler: Info message")
logger.error("Stream Handler: Error message")
try:
    raise RuntimeError("Test exception handling")
except RuntimeError as e:
    logger.exception(e)
# This should produce no output at all.

null_logger = logging.getLogger("null")
null_handler = logging.NullHandler()
null_logger.addHandler(null_handler)
assert null_logger.hasHandlers()

null_logger.setLevel(logging.ERROR)
null_logger.info("Null Handler: Info message")
null_logger.error("Null Handler: Error message")
try:
    raise RuntimeError("Test exception handling")
except RuntimeError as e:
    null_logger.exception(e)
