# SPDX-FileCopyrightText: 2020 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Used with ble_uart_echo_test.py. Transmits "echo" to the UARTService and receives it back.
"""

import binascii
import random
import time

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import (
    ProvideServicesAdvertisement,
    Advertisement,
)
import adafruit_ble_file_transfer


def _write(client, filename, contents, *, offset=0):
    # pylint: disable=redefined-outer-name
    start = time.monotonic()
    try:
        client.write(filename, contents, offset=offset)
        duration = time.monotonic() - start
        client = wait_for_reconnect()
    except RuntimeError:
        print("write failed. is usb connected?")
        return client
    print("wrote", filename, "at rate", len(contents) / duration, "B/s")
    return client


def _read(client, filename, *, offset=0):
    # pylint: disable=redefined-outer-name
    start = time.monotonic()
    try:
        contents = client.read(filename, offset=offset)
        duration = time.monotonic() - start
    except ValueError:
        print("missing file:", filename)
        return b""
    print("read", filename, "at rate", len(contents) / duration, "B/s")
    return contents


ble = BLERadio()

peer_address = None


def wait_for_reconnect():
    print("reconnecting", end="")
    while ble.connected:
        pass
    print(".", end="")
    new_connection = ble.connect(peer_address)
    print(".", end="")
    if not new_connection.paired:
        print(".", end="")
        new_connection.pair()
    new_service = new_connection[adafruit_ble_file_transfer.FileTransferService]
    new_client = adafruit_ble_file_transfer.FileTransferClient(new_service)
    print(".", end="")
    time.sleep(2)
    print("done")
    return new_client


# ble._adapter.erase_bonding()
# print("erased")
while True:
    try:
        while ble.connected:
            for connection in ble.connections:
                # pylint: disable=redefined-outer-name
                if adafruit_ble_file_transfer.FileTransferService not in connection:
                    continue
                if not connection.paired:
                    print("pairing")
                    connection.pair()
                print("paired")
                print()
                service = connection[adafruit_ble_file_transfer.FileTransferService]
                client = adafruit_ble_file_transfer.FileTransferClient(service)

                print("Testing write")
                client = _write(client, "/hello.txt", "Hello world".encode("utf-8"))
                time.sleep(1)
                c = _read(client, "/hello.txt")
                print(len(c), c)
                print()

                print("Testing mkdir")
                try:
                    client.mkdir("/world/")
                except ValueError:
                    print("path exists or isn't valid")
                print(client.listdir("/"))
                print(client.listdir("/world/"))
                print()

                print("Test writing within dir")
                client = _write(client, "/world/hi.txt", "Hi world".encode("utf-8"))

                hello_world = "Hello world".encode("utf-8")
                client = _write(client, "/world/hello.txt", hello_world)
                c = _read(client, "/world/hello.txt")
                print(c)
                print()

                # Test offsets
                print("Testing offsets")
                hello = len("Hello ".encode("utf-8"))
                c = _read(client, "/world/hello.txt", offset=hello)
                print(c)

                client = _write(
                    client, "/world/hello.txt", "offsets!".encode("utf-8"), offset=hello
                )
                c = _read(client, "/world/hello.txt", offset=0)
                print(c)
                print()

                # Test deleting
                print("Testing delete in /world/")
                print(client.listdir("/world/"))
                try:
                    client.delete("/world/hello.txt")
                except ValueError:
                    print("delete failed")

                try:
                    client.delete("/world/")
                    print("deleted /world/")
                except ValueError:
                    print("delete failed")
                print(client.listdir("/world/"))
                try:
                    client.delete("/world/hi.txt")
                except ValueError:
                    pass
                try:
                    client.delete("/world/")
                except ValueError:
                    pass
                print()

                # Test move
                print("Testing move")
                print(client.listdir("/"))
                try:
                    client.move("/hello.txt", "/world/hi.txt")
                except ValueError:
                    pass
                try:
                    client.move("/hello.txt", "/hi.txt")
                except ValueError:
                    print("move failed")
                print(client.listdir("/"))
                client.delete("/hi.txt")
                print()

                # Test larger files
                print("Testing larger files")
                large_1k = bytearray(1024)
                for i, _ in enumerate(large_1k):
                    large_1k[i] = random.randint(0, 255)
                client = _write(client, "/random.txt", large_1k)
                contents = _read(client, "/random.txt")
                if large_1k != contents:
                    print(binascii.hexlify(large_1k))
                    print(binascii.hexlify(contents))
                    raise RuntimeError("large contents don't match!")
                print()
            time.sleep(20)
    except ConnectionError as e:
        pass

    print("disconnected, scanning")
    for advertisement in ble.start_scan(
        ProvideServicesAdvertisement, Advertisement, timeout=1
    ):
        # print(advertisement.address, advertisement.address.type)
        if (
            not hasattr(advertisement, "services")
            or adafruit_ble_file_transfer.FileTransferService
            not in advertisement.services
        ):
            continue
        ble.connect(advertisement)
        peer_address = advertisement.address
        print("connected to", advertisement.address)
        break
    ble.stop_scan()
