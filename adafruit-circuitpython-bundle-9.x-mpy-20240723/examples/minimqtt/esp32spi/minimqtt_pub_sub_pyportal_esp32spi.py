# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import os
import time
import adafruit_connection_manager
import adafruit_pyportal

import adafruit_minimqtt.adafruit_minimqtt as MQTT

pyportal = adafruit_pyportal.PyPortal()

# Add settings.toml to your filesystem CIRCUITPY_WIFI_SSID and CIRCUITPY_WIFI_PASSWORD keys
# with your WiFi credentials. Add your Adafruit IO username and key as well.
# DO NOT share that file or commit it into Git or other source control.

aio_username = os.getenv("aio_username")
aio_key = os.getenv("aio_key")

# ------------- MQTT Topic Setup ------------- #
mqtt_topic = "test/topic"


### Code ###
# Define callback methods which are called when events occur
# pylint: disable=unused-argument, redefined-outer-name
def connected(client, userdata, flags, rc):
    # This function will be called when the client is connected
    # successfully to the broker.
    print("Subscribing to %s" % (mqtt_topic))
    client.subscribe(mqtt_topic)


def disconnected(client, userdata, rc):
    # This method is called when the client is disconnected
    print("Disconnected from MQTT Broker!")


def message(client, topic, message):
    """Method callled when a client's subscribed feed has a new
    value.
    :param str topic: The topic of the feed with a new value.
    :param str message: The new value
    """
    print("New message on topic {0}: {1}".format(topic, message))


# Connect to WiFi
print("Connecting to WiFi...")
pyportal.network.connect()
print("Connected!")

# pylint: disable=protected-access
pool = adafruit_connection_manager.get_radio_socketpool(pyportal.network._wifi.esp)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(
    pyportal.network._wifi.esp
)

# Set up a MiniMQTT Client
mqtt_client = MQTT.MQTT(
    broker=os.getenv("broker"),
    username=os.getenv("username"),
    password=os.getenv("password"),
    is_ssl=False,
    socket_pool=pool,
    ssl_context=ssl_context,
)

# Setup the callback methods above
mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected
mqtt_client.on_message = message

# Connect the client to the MQTT broker.
mqtt_client.connect()

photocell_val = 0
while True:
    # Poll the message queue
    mqtt_client.loop()

    # Send a new message
    print("Sending photocell value: %d" % photocell_val)
    mqtt_client.publish(mqtt_topic, photocell_val)
    photocell_val += 1
    time.sleep(1)
