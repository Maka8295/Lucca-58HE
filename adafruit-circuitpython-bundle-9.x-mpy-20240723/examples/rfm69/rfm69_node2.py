# SPDX-FileCopyrightText: 2020 Jerry Needell for Adafruit Industries
# SPDX-License-Identifier: MIT

# Example to send a packet periodically between addressed nodes

import time
import board
import busio
import digitalio
import adafruit_rfm69

# Define radio parameters.
RADIO_FREQ_MHZ = 915.0  # Frequency of the radio in Mhz. Must match your
# module! Can be a value like 915.0, 433.0, etc.

# Define pins connected to the chip.
CS = digitalio.DigitalInOut(board.CE1)
RESET = digitalio.DigitalInOut(board.D25)

# Initialize SPI bus.
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialze RFM radio
rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, RADIO_FREQ_MHZ)

# Optionally set an encryption key (16 byte AES key). MUST match both
# on the transmitter and receiver (or be set to None to disable/the default).
rfm69.encryption_key = (
    b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08"
)

# set node addresses
rfm69.node = 2
rfm69.destination = 1
# initialize counter
counter = 0
# send a broadcast message from my_node with ID = counter
rfm69.send(bytes("startup message from node {} ".format(rfm69.node), "UTF-8"))

# Wait to receive packets.
print("Waiting for packets...")
# initialize flag and timer
time_now = time.monotonic()
while True:
    # Look for a new packet: only accept if addresses to my_node
    packet = rfm69.receive(with_header=True)
    # If no packet was received during the timeout then None is returned.
    if packet is not None:
        # Received a packet!
        # Print out the raw bytes of the packet:
        print("Received (raw header):", [hex(x) for x in packet[0:4]])
        print("Received (raw payload): {0}".format(packet[4:]))
        print("Received RSSI: {0}".format(rfm69.last_rssi))
        # send reading after any packet received
        counter = counter + 1
        # after 10 messages send a response to destination_node from my_node with ID = counter&0xff
        if counter % 10 == 0:
            time.sleep(0.5)  # brief delay before responding
            rfm69.identifier = counter & 0xFF
            rfm69.send(
                bytes(
                    "message number {} from node {} ".format(counter, rfm69.node),
                    "UTF-8",
                ),
                keep_listening=True,
            )
