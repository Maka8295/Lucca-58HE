# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# import board
# import busio
# import digitalio
# import adafruit_mcp2515
# from adafruit_mcp2515.canio import Timer


from digitalio import DigitalInOut
from board import D5 as CS_PIN, SPI
from adafruit_mcp2515.canio import Timer, Message, RemoteTransmissionRequest
from adafruit_mcp2515 import MCP2515 as CAN

# from board import CAN_RX, CAN_TX


def bus():
    cs = DigitalInOut(CS_PIN)
    cs.switch_to_output()
    return CAN(SPI(), cs, loopback=True, silent=True)


mb1 = [0xDE, 0xAD, 0xBE, 0xEF]
mb2 = [0xCA, 0xFE, 0xFA, 0xDE]

t = Timer(timeout=5)
while True:
    with bus() as can, can.listen(timeout=1.0) as listener:

        mb1.insert(0, mb2.pop())
        mb2.insert(0, mb1.pop())
        message = Message(id=0xFFAA, data=bytes(mb1 + mb2), extended=True)
        rtr = RemoteTransmissionRequest(id=0x11FF, length=10)
        can.send(message)
        message_count = listener.in_waiting()
        print(message_count, "messages available")
        if message_count == 0:
            continue
        for _i in range(message_count):
            msg = listener.receive()
            print("Message from ", hex(msg.id))
            print("message data:", msg.data)
            message_str = "::".join(["0x{:02X}".format(i) for i in msg.data])
            print(message_str)

        # instead of sleeping, pool for messages to fill queue
        t.rewind_to(1)
        while not t.expired:
            message_count = listener.in_waiting()
