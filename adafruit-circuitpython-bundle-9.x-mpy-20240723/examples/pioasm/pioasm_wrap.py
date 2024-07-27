# SPDX-FileCopyrightText: 2022 Jeff Epler, written for Adafruit Industries
# SPDF-FileCopyrightText: 2020 Raspberry Pi (Trading) Ltd.
#
# SPDX-License-Identifier: BSD-3-Clause
import adafruit_pioasm

program = adafruit_pioasm.Program(
    """
    set pindirs, 1
.wrap_target
    set pins, 0
    set pins, 1
.wrap""",
    build_debuginfo=True,
)

program.print_c_program("test")
