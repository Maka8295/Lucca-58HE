# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import os
import time
import board
import busio
import digitalio
import adafruit_connection_manager
from adafruit_fona.adafruit_fona import FONA
import adafruit_fona.adafruit_fona_network as network
import adafruit_fona.adafruit_fona_socket as pool

import adafruit_minimqtt.adafruit_minimqtt as MQTT

# Add settings.toml to your filesystem CIRCUITPY_WIFI_SSID and CIRCUITPY_WIFI_PASSWORD keys
# with your GPRS credentials. Add your Adafruit IO username and key as well.
# DO NOT share that file or commit it into Git or other source control.

aio_username = os.getenv("aio_username")
aio_key = os.getenv("aio_key")

# Create a serial connection for the FONA connection
uart = busio.UART(board.TX, board.RX)
rst = digitalio.DigitalInOut(board.D4)
# Initialize FONA
fona = FONA(uart, rst)

### Topic Setup ###

# MQTT Topic
# Use this topic if you'd like to connect to a standard MQTT broker
mqtt_topic = "test/topic"

# Adafruit IO-style Topic
# Use this topic if you'd like to connect to io.adafruit.com
# mqtt_topic = 'aio_user/feeds/temperature'

### Code ###


# Define callback methods which are called when events occur
# pylint: disable=unused-argument, redefined-outer-name
def connect(client, userdata, flags, rc):
    # This function will be called when the client is connected
    # successfully to the broker.
    print("Connected to MQTT Broker!")
    print("Flags: {0}\n RC: {1}".format(flags, rc))


def disconnect(client, userdata, rc):
    # This method is called when the client disconnects
    # from the broker.
    print("Disconnected from MQTT Broker!")


def subscribe(client, userdata, topic, granted_qos):
    # This method is called when the client subscribes to a new feed.
    print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))


def unsubscribe(client, userdata, topic, pid):
    # This method is called when the client unsubscribes from a feed.
    print("Unsubscribed from {0} with PID {1}".format(topic, pid))


def publish(client, userdata, topic, pid):
    # This method is called when the client publishes data to a feed.
    print("Published to {0} with PID {1}".format(topic, pid))


# Initialize cellular data network
network = network.CELLULAR(
    fona, (os.getenv("apn"), os.getenv("apn_username"), os.getenv("apn_password"))
)

while not network.is_attached:
    print("Attaching to network...")
    time.sleep(0.5)
print("Attached!")

while not network.is_connected:
    print("Connecting to network...")
    network.connect()
    time.sleep(0.5)
print("Network Connected!")

ssl_context = adafruit_connection_manager.create_fake_ssl_context(pool, fona)

# Set up a MiniMQTT Client
client = MQTT.MQTT(
    broker=os.getenv("broker"),
    username=os.getenv("username"),
    password=os.getenv("password"),
    is_ssl=False,
    socket_pool=pool,
    ssl_context=ssl_context,
)

# Connect callback handlers to client
client.on_connect = connect
client.on_disconnect = disconnect
client.on_subscribe = subscribe
client.on_unsubscribe = unsubscribe
client.on_publish = publish

print("Attempting to connect to %s" % client.broker)
client.connect()

print("Subscribing to %s" % mqtt_topic)
client.subscribe(mqtt_topic)

print("Publishing to %s" % mqtt_topic)
client.publish(mqtt_topic, "Hello Broker!")

print("Unsubscribing from %s" % mqtt_topic)
client.unsubscribe(mqtt_topic)

print("Disconnecting from %s" % client.broker)
client.disconnect()
