# SPDX-FileCopyrightText: 2022 vladak
# SPDX-License-Identifier: Unlicense
"""
Demonstrate how to use a single logger to emit log records to
both console and MQTT broker, in this case Adafruit IO.
"""

import json
import socket
import ssl

import adafruit_minimqtt.adafruit_minimqtt as MQTT

import adafruit_logging as logging

# adafruit_logging defines log levels dynamically.
# pylint: disable=no-name-in-module
from adafruit_logging import NOTSET, Handler, LogRecord


class MQTTHandler(Handler):
    """
    Log handler that emits log records as MQTT PUBLISH messages.
    """

    def __init__(self, mqtt_client: MQTT.MQTT, topic: str) -> None:
        """
        Assumes that the MQTT client object is already connected.
        """
        super().__init__()

        self._mqtt_client = mqtt_client
        self._topic = topic

        # To make it work also in CPython.
        self.level = NOTSET

    def emit(self, record: LogRecord) -> None:
        """
        Publish message from the LogRecord to the MQTT broker, if connected.
        """
        try:
            if self._mqtt_client.is_connected():
                self._mqtt_client.publish(self._topic, record.msg)
        except MQTT.MMQTTException:
            pass

    # To make this work also in CPython's logging.
    def handle(self, record: LogRecord) -> None:
        """
        Handle the log record. Here, it means just emit.
        """
        self.emit(record)


def main():
    """
    Demonstrate how to use MQTT log handler.
    """
    logger = logging.getLogger(__name__)

    broker = "io.adafruit.com"
    port = 8883
    username = "Adafruit_IO_username"
    password = "Adafruit_IO_key"
    feedname = "Adafruit_feed_name"
    mqtt_topic = f"{username}/feeds/{feedname}"
    mqtt_client = MQTT.MQTT(
        broker=broker,
        port=port,
        username=username,
        password=password,
        socket_pool=socket,
        ssl_context=ssl.create_default_context(),
    )
    mqtt_client.connect()
    mqtt_handler = MQTTHandler(mqtt_client, mqtt_topic)
    print("adding MQTT handler")
    logger.addHandler(mqtt_handler)

    stream_handler = logging.StreamHandler()
    print("adding Stream handler")
    logger.addHandler(stream_handler)

    data = "foo bar"
    print("logging begins !")
    # This should emit both to the console as well as to the MQTT broker.
    logger.warning(json.dumps(data))


if __name__ == "__main__":
    main()
