# SPDX-FileCopyrightText: 2022 Michał Pokusa
#
# SPDX-License-Identifier: Unlicense

import socketpool
import wifi

from adafruit_httpserver import Server, Request, ChunkedResponse


pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, debug=True)


@server.route("/chunked")
def chunked(request: Request):
    """
    Return the response with ``Transfer-Encoding: chunked``.
    """

    def body():
        yield "Adaf"
        yield b"ruit"  # Data chunk can be bytes or str.
        yield " Indus"
        yield b"tr"
        yield "ies"

    return ChunkedResponse(request, body)


server.serve_forever(str(wifi.radio.ipv4_address))
