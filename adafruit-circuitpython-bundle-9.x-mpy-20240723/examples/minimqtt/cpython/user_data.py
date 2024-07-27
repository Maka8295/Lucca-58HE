# SPDX-FileCopyrightText: 2023 Vladimír Kotal
# SPDX-License-Identifier: Unlicense

# pylint: disable=logging-fstring-interpolation

"""
Demonstrate on how to use user_data for various callbacks.
"""

import logging
import socket
import ssl
import sys

import adafruit_minimqtt.adafruit_minimqtt as MQTT


# pylint: disable=unused-argument
def on_connect(mqtt_client, user_data, flags, ret_code):
    """
    connect callback
    """
    logger = logging.getLogger(__name__)
    logger.debug("Connected to MQTT Broker!")
    logger.debug(f"Flags: {flags}\n RC: {ret_code}")


# pylint: disable=unused-argument
def on_subscribe(mqtt_client, user_data, topic, granted_qos):
    """
    subscribe callback
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"Subscribed to {topic} with QOS level {granted_qos}")


def on_message(client, topic, message):
    """
    received message callback
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"New message on topic {topic}: {message}")

    messages = client.user_data
    if not messages.get(topic):
        messages[topic] = []
    messages[topic].append(message)


# pylint: disable=too-many-statements,too-many-locals
def main():
    """
    Main loop.
    """

    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # dictionary/map of topic to list of messages
    messages = {}

    # connect to MQTT broker
    mqtt = MQTT.MQTT(
        broker="172.40.0.3",
        port=1883,
        socket_pool=socket,
        ssl_context=ssl.create_default_context(),
        user_data=messages,
    )

    mqtt.on_connect = on_connect
    mqtt.on_subscribe = on_subscribe
    mqtt.on_message = on_message

    logger.info("Connecting to MQTT broker")
    mqtt.connect()
    logger.info("Subscribing")
    mqtt.subscribe("foo/#", qos=0)
    mqtt.add_topic_callback("foo/bar", on_message)

    i = 0
    while True:
        i += 1
        logger.debug(f"Loop {i}")
        # Make sure to stay connected to the broker e.g. in case of keep alive.
        mqtt.loop(1)

        for topic, msg_list in messages.items():
            logger.info(f"Got {len(msg_list)} messages from topic {topic}")
            for msg_cnt, msg in enumerate(msg_list):
                logger.debug(f"#{msg_cnt}: {msg}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
