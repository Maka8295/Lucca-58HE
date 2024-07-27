# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Circuit Playground Express Demo Code
# Adjust the pulseio 'board.PIN' if using something else
import time

import board
import pulseio

import adafruit_irremote

pulsein = pulseio.PulseIn(board.REMOTEIN, maxlen=120, idle_state=True)
decoder = adafruit_irremote.NonblockingGenericDecode(pulsein)


t0 = next_heartbeat = time.monotonic()

while True:
    for message in decoder.read():
        print(f"t={time.monotonic() - t0:.3} New Message")
        print("Heard", len(message.pulses), "Pulses:", message.pulses)
        if isinstance(message, adafruit_irremote.IRMessage):
            print("Decoded:", message.code)
        elif isinstance(message, adafruit_irremote.NECRepeatIRMessage):
            print("NEC repeat!")
        elif isinstance(message, adafruit_irremote.UnparseableIRMessage):
            print("Failed to decode", message.reason)
        print("----------------------------")

    # This heartbeat confirms that we are not blocked somewhere above.
    t = time.monotonic()
    if t > next_heartbeat:
        print(f"t={time.monotonic() - t0:.3} Heartbeat")
        next_heartbeat = t + 0.1
