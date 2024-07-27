# SPDX-FileCopyrightText: 2023 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import asyncio
import binascii
import os

import espcamera
import socketpool
import wifi
from adafruit_httpserver.response import ChunkedResponse
from adafruit_httpserver.server import Server

import adafruit_pycamera

pycam = adafruit_pycamera.PyCamera()
pycam.camera.reconfigure(
    pixel_format=espcamera.PixelFormat.JPEG,
    frame_size=espcamera.FrameSize.SVGA,
)
pycam.camera.quality = 6

server = Server(socketpool.SocketPool(wifi.radio))
if wifi.radio.ipv4_address:
    # use alt port if web workflow enabled
    port = 8080
else:
    # connect to wifi and use standard http port otherwise
    wifi.radio.connect(os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD"))
    port = 80

BOUNDARY = b"FRAME" + binascii.hexlify(os.urandom(8))


@server.route("/")
def base(request):
    def body():
        while True:
            jpeg = pycam.camera.take()
            yield b"--"
            yield BOUNDARY
            yield b"\r\n"
            yield b"Content-Type: image/jpeg\r\nContent-Length: "
            yield str(len(jpeg))
            yield "\r\n\r\n"
            yield jpeg
            yield "\r\n"

    return ChunkedResponse(
        request,
        body,
        headers={
            "Content-Type": "multipart/x-mixed-replace; boundary=%s"
            % BOUNDARY.decode("ascii")
        },
    )


async def poll(interval):
    server.start(str(wifi.radio.ipv4_address), port=port)
    while True:
        try:
            server.poll()
        except BrokenPipeError as e:
            print(e)
        await asyncio.sleep(interval)


async def main():
    poll_task = asyncio.create_task(poll(0))
    await asyncio.gather(poll_task)


pycam.display_message(f"{wifi.radio.ipv4_address}:{port}/", scale=2)

asyncio.run(main())
