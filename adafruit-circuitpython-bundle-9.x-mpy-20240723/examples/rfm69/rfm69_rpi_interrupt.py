# SPDX-FileCopyrightText: 2020 Tony DiCola, Jerry Needell for Adafruit Industries
# SPDX-License-Identifier: MIT

# Example using Interrupts to send a message and then wait indefinitely for messages
# to be received. Interrupts are used only for receive. sending is done with polling.
# This example is for systems that support interrupts like the Raspberry Pi with "blinka"
# CircuitPython does not support interrupts so it will not work on  Circutpython boards
import time
import board
import busio
import digitalio
import RPi.GPIO as io
import adafruit_rfm69


# setup interrupt callback function
def rfm69_callback(rfm69_irq):
    global packet_received  # pylint: disable=global-statement
    print(
        "IRQ detected on pin {0} payload_ready {1} ".format(
            rfm69_irq, rfm69.payload_ready
        )
    )
    # see if this was a payload_ready interrupt ignore if not
    if rfm69.payload_ready:
        packet = rfm69.receive(timeout=None)
        if packet is not None:
            # Received a packet!
            packet_received = True
            # Print out the raw bytes of the packet:
            print("Received (raw bytes): {0}".format(packet))
            print([hex(x) for x in packet])
            print("RSSI: {0}".format(rfm69.last_rssi))


# Define radio parameters.
RADIO_FREQ_MHZ = 915.0  # Frequency of the radio in Mhz. Must match your
# module! Can be a value like 915.0, 433.0, etc.

# Define pins connected to the chip, use these if wiring up the breakout according to the guide:
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

# Print out some chip state:
print("Temperature: {0}C".format(rfm69.temperature))
print("Frequency: {0}mhz".format(rfm69.frequency_mhz))
print("Bit rate: {0}kbit/s".format(rfm69.bitrate / 1000))
print("Frequency deviation: {0}hz".format(rfm69.frequency_deviation))

# configure the interrupt pin and event handling.
RFM69_G0 = 22
io.setmode(io.BCM)
io.setup(RFM69_G0, io.IN, pull_up_down=io.PUD_DOWN)  # activate input
io.add_event_detect(RFM69_G0, io.RISING)
io.add_event_callback(RFM69_G0, rfm69_callback)
packet_received = False

# Send a packet.  Note you can only send a packet up to 60 bytes in length.
# This is a limitation of the radio packet size, so if you need to send larger
# amounts of data you will need to break it into smaller send calls.  Each send
# call will wait for the previous one to finish before continuing.
rfm69.send(bytes("Hello world!\r\n", "utf-8"), keep_listening=True)
print("Sent hello world message!")
# If you don't wawnt to send a message to start you can just start lintening
# rmf69.listen()

# Wait to receive packets.  Note that this library can't receive data at a fast
# rate, in fact it can only receive and process one 60 byte packet at a time.
# This means you should only use this for low bandwidth scenarios, like sending
# and receiving a single message at a time.
print("Waiting for packets...")

# the loop is where you can do any desire processing
# the global variable packet_received can be used to determine if a packet was received.
while True:
    # the sleep time is arbitrary since any incomming packe will trigger an interrupt
    # and be received.
    time.sleep(0.1)
    if packet_received:
        print("received message!")
        packet_received = False
