# SPDX-FileCopyrightText: 2023 Michał Pokusa
#
# SPDX-License-Identifier: Unlicense

import socketpool
import wifi

from adafruit_httpserver import Server, Request, Response


pool = socketpool.SocketPool(wifi.radio)

bedroom_server = Server(pool, "/bedroom", debug=True)
bedroom_server.headers["X-Server"] = "Bedroom"

office_server = Server(pool, "/office", debug=True)
office_server.headers["X-Server"] = "Office"


@bedroom_server.route("/bedroom")
def bedroom(request: Request):
    """
    This route is registered only on ``bedroom_server``.
    """
    return Response(request, "Hello from the bedroom!")


@office_server.route("/office")
def office(request: Request):
    """
    This route is registered only on ``office_server``.
    """
    return Response(request, "Hello from the office!")


@bedroom_server.route("/home")
@office_server.route("/home")
def home(request: Request):
    """
    This route is registered on both servers.
    """
    return Response(request, "Hello from home!")


id_address = str(wifi.radio.ipv4_address)

# Start the servers.
bedroom_server.start(id_address, 5000)
office_server.start(id_address, 8000)

while True:
    try:
        # Process any waiting requests for both servers.
        bedroom_server.poll()
        office_server.poll()
    except OSError as error:
        print(error)
        continue
