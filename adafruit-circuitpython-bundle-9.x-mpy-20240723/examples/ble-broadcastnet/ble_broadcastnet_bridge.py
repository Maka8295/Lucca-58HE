# SPDX-FileCopyrightText: 2022 Scott Shawcroft for Adafruit Industries
# SPDX-License-Identifier: MIT

"""This example bridges from BLE to Adafruit IO on a CircuitPython device that
   supports both WiFi and BLE. (The first chip is the ESP32-S3.)"""
from secrets import secrets  # pylint: disable=no-name-in-module
import ssl
import time
import adafruit_requests as requests
from adafruit_ble.advertising.standard import ManufacturerDataField
import adafruit_ble
import board
import socketpool
import wifi
import adafruit_ble_broadcastnet

# To get a status neopixel flashing, install the neopixel library as well.

if hasattr(board, "NEOPIXEL"):
    try:
        import neopixel
        import rainbowio
    except ImportError:
        print("No status pixel due to missing library")
        neopixel = None

aio_auth_header = {"X-AIO-KEY": secrets["aio_key"]}
aio_base_url = "https://io.adafruit.com/api/v2/" + secrets["aio_username"]

print("Connecting to %s" % secrets["ssid"])
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Connected to %s!" % secrets["ssid"])
print("My IP address is", wifi.radio.ipv4_address)

socket = socketpool.SocketPool(wifi.radio)
https = requests.Session(socket, ssl.create_default_context())

status_pixel = None
if neopixel and hasattr(board, "NEOPIXEL"):
    status_pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.02)


def aio_post(path, **kwargs):
    kwargs["headers"] = aio_auth_header
    return https.post(aio_base_url + path, **kwargs)


def aio_get(path, **kwargs):
    kwargs["headers"] = aio_auth_header
    return https.get(aio_base_url + path, **kwargs)


# Disable outer names check because we frequently collide.
# pylint: disable=redefined-outer-name


def create_group(name):
    response = aio_post("/groups", json={"name": name})
    if response.status_code != 201:
        print(name)
        print(response.content)
        print(response.status_code)
        raise RuntimeError("unable to create new group")
    return response.json()["key"]


def create_feed(group_key, name):
    response = aio_post(
        "/groups/{}/feeds".format(group_key), json={"feed": {"name": name}}
    )
    if response.status_code != 201:
        print(name)
        print(response.content)
        print(response.status_code)
        raise RuntimeError("unable to create new feed")
    return response.json()["key"]


def create_data(group_key, data):
    response = aio_post("/groups/{}/data".format(group_key), json={"feeds": data})
    if response.status_code == 429:
        print("Throttled!")
        return False
    if response.status_code != 200:
        print(response.status_code, response.json())
        raise RuntimeError("unable to create new data")
    response.close()
    return True


def convert_to_feed_data(values, attribute_name, attribute_instance):
    feed_data = []
    # Wrap single value entries for enumeration.
    if not isinstance(values, tuple) or (
        attribute_instance.element_count > 1 and not isinstance(values[0], tuple)
    ):
        values = (values,)
    for i, value in enumerate(values):
        key = attribute_name.replace("_", "-") + "-" + str(i)
        if isinstance(value, tuple):
            for j in range(attribute_instance.element_count):
                feed_data.append(
                    {
                        "key": key + "-" + attribute_instance.field_names[j],
                        "value": value[j],
                    }
                )
        else:
            feed_data.append({"key": key, "value": value})
    return feed_data


ble = adafruit_ble.BLERadio()
bridge_address = adafruit_ble_broadcastnet.device_address
print("This is BroadcastNet bridge:", bridge_address)
print()

print("Fetching existing feeds for this bridge.")

existing_feeds = {}
response = aio_get("/groups")
for group in response.json():
    if "-" not in group["key"]:
        continue
    pieces = group["key"].split("-")
    if len(pieces) != 4 or pieces[0] != "bridge" or pieces[2] != "sensor":
        continue
    _, bridge, _, sensor_address = pieces
    if bridge != bridge_address:
        continue
    existing_feeds[sensor_address] = []
    for feed in group["feeds"]:
        feed_key = feed["key"].split(".")[-1]
        existing_feeds[sensor_address].append(feed_key)

print(existing_feeds)

print("scanning")
print()
sequence_numbers = {}
# By providing Advertisement as well we include everything, not just specific advertisements.
for measurement in ble.start_scan(
    adafruit_ble_broadcastnet.AdafruitSensorMeasurement, interval=0.5
):
    reversed_address = [measurement.address.address_bytes[i] for i in range(5, -1, -1)]
    sensor_address = "{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(*reversed_address)
    if sensor_address not in sequence_numbers:
        sequence_numbers[sensor_address] = measurement.sequence_number - 1 % 256
    # Skip if we are getting the same broadcast more than once.
    if measurement.sequence_number == sequence_numbers[sensor_address]:
        continue
    number_missed = measurement.sequence_number - sequence_numbers[sensor_address] - 1
    if number_missed < 0:
        number_missed += 256
    # Derive the status color from the sensor address.
    if status_pixel:
        status_pixel[0] = rainbowio.colorwheel(sum(reversed_address))
    group_key = "bridge-{}-sensor-{}".format(bridge_address, sensor_address)
    if sensor_address not in existing_feeds:
        create_group("Bridge {} Sensor {}".format(bridge_address, sensor_address))
        create_feed(group_key, "Missed Message Count")
        existing_feeds[sensor_address] = ["missed-message-count"]

    data = [{"key": "missed-message-count", "value": number_missed}]
    for attribute in dir(measurement.__class__):
        attribute_instance = getattr(measurement.__class__, attribute)
        if issubclass(attribute_instance.__class__, ManufacturerDataField):
            if attribute != "sequence_number":
                values = getattr(measurement, attribute)
                if values is not None:
                    data.extend(
                        convert_to_feed_data(values, attribute, attribute_instance)
                    )

    for feed_data in data:
        if feed_data["key"] not in existing_feeds[sensor_address]:
            create_feed(group_key, feed_data["key"])
            existing_feeds[sensor_address].append(feed_data["key"])

    start_time = time.monotonic()
    print(group_key, data)
    # Only update the previous sequence if we logged successfully.
    if create_data(group_key, data):
        sequence_numbers[sensor_address] = measurement.sequence_number

    duration = time.monotonic() - start_time
    if status_pixel:
        status_pixel[0] = 0x000000
    print("Done logging measurement to IO. Took {} seconds".format(duration))
    print()

print("scan done")
