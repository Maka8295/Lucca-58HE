# SPDX-FileCopyrightText: Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2019 Brent Rubell for Adafruit Industries
# SPDX-License-Identifier: MIT

# Example of using the Adafruit IO CircuitPython MQTT client
# to subscribe to an Adafruit IO feed and publish random data
# to be received by the feed.
import time
from random import randint

import board
import busio
import digitalio

import adafruit_connection_manager
from adafruit_fona.adafruit_fona import FONA
from adafruit_fona.adafruit_fona_gsm import GSM
import adafruit_fona.adafruit_fona_socket as pool

import adafruit_minimqtt.adafruit_minimqtt as MQTT
from adafruit_io.adafruit_io import IO_MQTT

# Get MQTT details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("MQTT secrets are kept in secrets.py, please add them there!")
    raise

# Create a serial connection for the FONA connection
uart = busio.UART(board.TX, board.RX)
rst = digitalio.DigitalInOut(board.D4)

# Initialize FONA module (this may take a few seconds)
fona = FONA(uart, rst)

# initialize gsm
gsm = GSM(fona, (secrets["apn"], secrets["apn_username"], secrets["apn_password"]))

while not gsm.is_attached:
    print("Attaching to network...")
    time.sleep(0.5)

while not gsm.is_connected:
    print("Connecting to network...")
    gsm.connect()
    time.sleep(5)


# Define callback functions which will be called when certain events happen.
# pylint: disable=unused-argument
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print("Connected to Adafruit IO!  Listening for DemoFeed changes...")
    # Subscribe to changes on a feed named DemoFeed.
    client.subscribe("DemoFeed")


# pylint: disable=unused-argument
def subscribe(client, userdata, topic, granted_qos):
    # This method is called when the client subscribes to a new feed.
    print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))


# pylint: disable=unused-argument
def unsubscribe(client, userdata, topic, pid):
    # This method is called when the client unsubscribes from a feed.
    print("Unsubscribed from {0} with PID {1}".format(topic, pid))


# pylint: disable=unused-argument
def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print("Disconnected from Adafruit IO!")


# pylint: disable=unused-argument
def publish(client, userdata, topic, pid):
    # This method is called when the client publishes data to a feed.
    print("Published to {0} with PID {1}".format(topic, pid))
    if userdata is not None:
        print("Published User data: ", end="")
        print(userdata)


# pylint: disable=unused-argument
def message(client, feed_id, payload):
    # Message function will be called when a subscribed feed has a new value.
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.
    print("Feed {0} received new value: {1}".format(feed_id, payload))


ssl_context = adafruit_connection_manager.create_fake_ssl_context(pool, fona)

# Initialize a new MQTT Client object
mqtt_client = MQTT.MQTT(
    broker="io.adafruit.com",
    port=1883,
    username=secrets["aio_username"],
    password=secrets["aio_key"],
    socket_pool=pool,
    ssl_context=ssl_context,
)

# Initialize an Adafruit IO MQTT Client
io = IO_MQTT(mqtt_client)

# Connect the callback methods defined above to Adafruit IO
io.on_connect = connected
io.on_disconnect = disconnected
io.on_subscribe = subscribe
io.on_unsubscribe = unsubscribe
io.on_message = message
io.on_publish = publish

# Connect to Adafruit IO
print("Connecting to Adafruit IO...")
io.connect()

# Below is an example of manually publishing a new  value to Adafruit IO.
last = 0
print("Publishing a new message every 10 seconds...")
while True:
    # Explicitly pump the message loop.
    io.loop()
    # Send a new message every 10 seconds.
    if (time.monotonic() - last) >= 5:
        value = randint(0, 100)
        print("Publishing {0} to DemoFeed.".format(value))
        io.publish("DemoFeed", value)
        last = time.monotonic()
