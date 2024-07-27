# SPDX-FileCopyrightText: 2024 Michał Pokusa
#
# SPDX-License-Identifier: Unlicense

import socket

from adafruit_httpserver import Server, Request, Response


pool = socket
server = Server(pool, "/static", debug=True)


@server.route("/")
def base(request: Request):
    """
    Serve a default static plain text message.
    """
    return Response(request, "Hello from the CircuitPython HTTP Server!")


# Ports below 1024 are reserved for root user only.
# If you want to run this example on a port below 1024, you need to run it as root (or with `sudo`).
server.serve_forever("0.0.0.0", 5000)
