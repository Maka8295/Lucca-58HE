# SPDX-FileCopyrightText: 2023 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import json
import os

import espcamera
import socketpool

# Disable autoreload. this is very handy while editing the js & html files
# as you want to just reload the web browser, not the CircutPython program!
import supervisor
import wifi
from adafruit_httpserver import (
    BAD_REQUEST_400,
    GET,
    INTERNAL_SERVER_ERROR_500,
    POST,
    FileResponse,
    JSONResponse,
    Request,
    Response,
    Server,
)

import adafruit_pycamera

supervisor.runtime.autoreload = False

pycam = adafruit_pycamera.PyCamera()

if wifi.radio.ipv4_address:
    # use alt port if web workflow enabled
    port = 8080
else:
    # connect to wifi and use standard http port otherwise
    wifi.radio.connect(os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD"))
    port = 80

print(wifi.radio.ipv4_address)

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, debug=True, root_path="/htdocs")


@server.route("/metadata.json", [GET])
def metadata(request: Request) -> Response:
    return FileResponse(request, "/metadata.js")


@server.route("/", [GET])
def index(request: Request) -> Response:
    return FileResponse(request, "/index.html")


@server.route("/index.js", [GET])
def index_js(request: Request) -> Response:
    return FileResponse(request, "/index.js")


@server.route("/lcd", [GET, POST])
def lcd(request: Request) -> Response:
    pycam.blit(pycam.continuous_capture())
    return Response(request, "")


@server.route("/jpeg", [GET, POST])
def take_jpeg(request: Request) -> Response:
    pycam.camera.reconfigure(
        pixel_format=espcamera.PixelFormat.JPEG,
        frame_size=pycam.resolution_to_frame_size[
            pycam._resolution  # pylint: disable=protected-access
        ],
    )
    try:
        jpeg = pycam.camera.take(1)
        if jpeg is not None:
            return Response(request, bytes(jpeg), content_type="image/jpeg")
        return Response(
            request, "", content_type="text/plain", status=INTERNAL_SERVER_ERROR_500
        )
    finally:
        pycam.live_preview_mode()


@server.route("/focus", [GET])
def focus(request: Request) -> Response:
    return JSONResponse(request, pycam.autofocus())


@server.route("/property", [GET, POST])
def property1(request: Request) -> Response:
    return property_common(pycam, request)


@server.route("/property2", [GET, POST])
def property2(request: Request) -> Response:
    return property_common(pycam.camera, request)


def property_common(obj, request):
    try:
        params = request.query_params or request.form_data
        propname = params["k"]
        value = params.get("v", None)

        if value is None:
            try:
                current_value = getattr(obj, propname, None)
                return JSONResponse(request, current_value)
            except Exception as exc:  # pylint: disable=broad-exception-caught
                return Response(request, {"error": str(exc)}, status=BAD_REQUEST_400)
        else:
            new_value = json.loads(value)
            setattr(obj, propname, new_value)
            return JSONResponse(request, {"status": "OK"})
    except Exception as exc:  # pylint: disable=broad-exception-caught
        return JSONResponse(request, {"error": str(exc)}, status=BAD_REQUEST_400)


pycam.display_message(f"{wifi.radio.ipv4_address}:{port}/", scale=2)
server.serve_forever(str(wifi.radio.ipv4_address), port)
