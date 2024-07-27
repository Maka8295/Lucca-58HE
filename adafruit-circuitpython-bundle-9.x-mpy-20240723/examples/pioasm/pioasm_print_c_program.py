# SPDX-FileCopyrightText: 2021 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: 2022 Jeff Epler, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import adafruit_pioasm

# NeoPixels are 800khz bit streams. Zeroes are 1/3 duty cycle (~416ns) and ones
# are 2/3 duty cycle (~833ns).
text_program = """
.program ws2812
.side_set 1
.wrap_target
bitloop:
  out x 1        side 0 [1]; Side-set still takes place when instruction stalls
  jmp !x do_zero side 1 [1]; Branch on the bit we shifted out. Positive pulse
do_one:
  jmp  bitloop   side 1 [1]; Continue driving high, for a long pulse
do_zero:
  nop            side 0 [1]; Or drive low, for a short pulse
.wrap
"""

program = adafruit_pioasm.Program(text_program, build_debuginfo=True)
program.print_c_program("pio_ws2812", qualifier="static const")

program = adafruit_pioasm.Program(text_program, build_debuginfo=False)
program.print_c_program("pio_ws2812_short")
