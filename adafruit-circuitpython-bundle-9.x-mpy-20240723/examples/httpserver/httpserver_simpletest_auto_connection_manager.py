# SPDX-FileCopyrightText: 2024 DJDevon3
#
# SPDX-License-Identifier: MIT

import wifi

from adafruit_connection_manager import get_radio_socketpool
from adafruit_httpserver import Server, Request, Response


pool = get_radio_socketpool(wifi.radio)
server = Server(pool, "/static", debug=True)


@server.route("/")
def base(request: Request):
    """
    Serve a default static plain text message.
    """
    return Response(request, "Hello from the CircuitPython HTTP Server!")


server.serve_forever(str(wifi.radio.ipv4_address))
