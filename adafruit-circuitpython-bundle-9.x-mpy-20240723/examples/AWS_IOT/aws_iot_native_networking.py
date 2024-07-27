# SPDX-FileCopyrightText: 2023 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import ssl
import json
import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from adafruit_aws_iot import MQTT_CLIENT

# Add a secrets.py to your filesystem that has a dictionary called "secrets". DO NOT share that
# file or commit it into Git or other source control. The "secrets" dictionary should have the
# following keys:
# "ssid" - Your WiFi ssid
# "password" - Your WiFi password
# "device_cert_path" - Path to the Device Certificate from AWS IoT ("<THING_NAME>.cert.pem")
# "device_key_path" - Path to the RSA Private Key from AWS IoT ("<THING_NAME>.private.key")
# "broker" - The endpoint for the AWS IoT broker ("<PREFIX>.iot.<REGION>.amazonaws.com")
# "client_id" - The client id. Your device's Policy needs to allow this client ("basicPubSub")
#
# pylint: disable=no-name-in-module,wrong-import-order
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

### Code ###

# Your device's Policy needs to allow this topic
topic = "sdk/test/python"


# Define callback methods which are called when events occur
# pylint: disable=unused-argument, redefined-outer-name
def connect(client, userdata, flags, rc):
    # This function will be called when the client is connected
    # successfully to the broker.
    print("Connected to MQTT Broker!")
    print("Flags: {0} - RC: {1}".format(flags, rc))

    # Subscribe to topic circuitpython/aws
    print("Subscribing to topic {}".format(topic))
    aws_iot.subscribe(topic)


def disconnect(client, userdata, rc):
    # This method is called when the client disconnects
    # from the broker.
    print("Disconnected from MQTT Broker!")


def subscribe(client, userdata, topic, granted_qos):
    # This method is called when the client subscribes to a new topic.
    print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))

    # Create a json-formatted message
    message = {"message": "Hello from AWS IoT CircuitPython"}
    # Publish message to topic
    aws_iot.publish(topic, json.dumps(message))


def unsubscribe(client, userdata, topic, pid):
    # This method is called when the client unsubscribes from a topic.
    print("Unsubscribed from {0} with PID {1}".format(topic, pid))


def publish(client, userdata, topic, pid):
    # This method is called when the client publishes data to a topic.
    print("Published to {0} with PID {1}".format(topic, pid))


def message(client, topic, msg):
    # This method is called when the client receives data from a topic.
    print("Message from {}: {}".format(topic, msg))


print("Connecting to %s" % secrets["ssid"])
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Connected to %s!" % secrets["ssid"])

# Create a socket pool
pool = socketpool.SocketPool(wifi.radio)
ssl_context = ssl.create_default_context()

# Set AWS Device Certificate and AWS RSA Private Key
ssl_context.load_cert_chain(
    certfile=secrets["device_cert_path"], keyfile=secrets["device_key_path"]
)

# Set up a MiniMQTT Client
mqtt_client = MQTT.MQTT(
    broker=secrets["broker"],
    client_id=secrets["client_id"],
    is_ssl=True,
    socket_pool=pool,
    ssl_context=ssl_context,
)

# Initialize AWS IoT MQTT API Client
aws_iot = MQTT_CLIENT(mqtt_client)

# Connect callback handlers to AWS IoT MQTT Client
aws_iot.on_connect = connect
aws_iot.on_disconnect = disconnect
aws_iot.on_subscribe = subscribe
aws_iot.on_unsubscribe = unsubscribe
aws_iot.on_publish = publish
aws_iot.on_message = message

print("Attempting to connect to %s" % mqtt_client.broker)
aws_iot.connect()

# Start a blocking message loop...
# NOTE: NO code below this loop will execute
# NOTE: Network reconnection is NOT handled within this loop
while True:
    aws_iot.loop(10)

    time.sleep(1)
