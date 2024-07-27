# SPDX-FileCopyrightText: 2022 Taxelas
# SPDX-License-Identifier: MIT
"""
python script to read mcp9808 temperature and publish it in mqtt.
Using discovery topic to create entity in Home Assistant.
"""

import time
import json
from array import array
import board
import paho.mqtt.client as mqtt
import numpy as np
import adafruit_mcp9808


i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

# To initialise using the default address:
mcp = adafruit_mcp9808.MCP9808(i2c)

broker_address = "Broker IP"
port = 1883
user = "mqttuser"
password = "mqttpassword"
client = mqtt.Client("P1")  # create new instance
client.username_pw_set(user, password=password)
client.connect(broker_address, port=port)
client.loop_start()
# To initialise using a specified address:
# Necessary when, for example, connecting A0 to VDD to make address=0x19
# mcp = adafruit_mcp9808.MCP9808(i2c_bus, address=0x19)


# Create autodiscovery topic for Home assistant
# "ha" is autodiscovery prefix in home assistant
send_msg = {
    "state_topic": "ha/sensor/sensorLivingroom/state",
    "device_class": "temperature",
    "unit_of_measurement": "°C",
    "value_template": "{{ value_json.temperature }}",
    "device": {
        "identifiers": ["rpisensorgatewayn01"],
        "manufacturer": "Raspberry",
        "model": "RPI 3B",
        "name": "Livingroom temperature",
        "sw_version": "MCU9808",
    },
    "name": "Livingroom temperature",
    "unique_id": "rpisensorgateway_0x01",
}
client.publish(
    "ha/sensor/sensorLivingroom/config",
    payload=json.dumps(send_msg),
    qos=0,
    retain=True,
)  # publish
temp1m = array(
    "d", [0, 0, 0, 0, 0, 0, 0, 0, 0]
)  # using array to aproximate 10 temperature readings
avgtemp = 0
while True:
    print(len(temp1m))
    for count in range(0, 9):
        temp1m[count] = mcp.temperature
        print("Temperature: {} C ".format(mcp.temperature))
        avgtemp = round(np.average(temp1m), 1)
        print("avgtemp {} C".format(avgtemp))
        time.sleep(10)
    send_msg = {"temperature": avgtemp}
    client.publish(
        "ha/sensor/sensorLivingroom/state", payload=json.dumps(send_msg)
    )  # publish result in mqtt
