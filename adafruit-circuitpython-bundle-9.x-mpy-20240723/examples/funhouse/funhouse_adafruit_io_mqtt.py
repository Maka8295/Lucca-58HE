# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import time
from adafruit_funhouse import FunHouse

funhouse = FunHouse(default_bg=None)
funhouse.peripherals.set_dotstars(0x800000, 0x808000, 0x008000, 0x000080, 0x800080)


# pylint: disable=unused-argument
def connected(client):
    print("Connected to Adafruit IO! Subscribing...")
    client.subscribe("buzzer")
    client.subscribe("neopixels")


def subscribe(client, userdata, topic, granted_qos):
    print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))


def disconnected(client):
    print("Disconnected from Adafruit IO!")


def message(client, feed_id, payload):
    print("Feed {0} received new value: {1}".format(feed_id, payload))
    if feed_id == "buzzer":
        if int(payload) == 1:
            funhouse.peripherals.play_tone(2000, 0.25)
    if feed_id == "neopixels":
        print(payload)
        color = int(payload[1:], 16)
        funhouse.peripherals.dotstars.fill(color)


# pylint: enable=unused-argument

# Initialize a new MQTT Client object
funhouse.network.init_io_mqtt()
funhouse.network.on_mqtt_connect = connected
funhouse.network.on_mqtt_disconnect = disconnected
funhouse.network.on_mqtt_subscribe = subscribe
funhouse.network.on_mqtt_message = message

print("Connecting to Adafruit IO...")
funhouse.network.mqtt_connect()
sensorwrite_timestamp = time.monotonic()
last_pir = None

while True:
    funhouse.network.mqtt_loop()

    print("Temp %0.1F" % funhouse.peripherals.temperature)
    print("Pres %d" % funhouse.peripherals.pressure)

    # every 10 seconds, write temp/hum/press
    if (time.monotonic() - sensorwrite_timestamp) > 10:
        funhouse.peripherals.led = True
        print("Sending data to adafruit IO!")
        funhouse.network.mqtt_publish("temperature", funhouse.peripherals.temperature)
        funhouse.network.mqtt_publish(
            "humidity", int(funhouse.peripherals.relative_humidity)
        )
        funhouse.network.mqtt_publish("pressure", int(funhouse.peripherals.pressure))
        sensorwrite_timestamp = time.monotonic()
        # Send PIR only if changed!
        if last_pir is None or last_pir != funhouse.peripherals.pir_sensor:
            last_pir = funhouse.peripherals.pir_sensor
            funhouse.network.mqtt_publish("pir", "%d" % last_pir)
        funhouse.peripherals.led = False
