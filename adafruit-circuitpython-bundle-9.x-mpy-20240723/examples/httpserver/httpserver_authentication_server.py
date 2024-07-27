# SPDX-FileCopyrightText: 2023 Michał Pokusa
#
# SPDX-License-Identifier: Unlicense

import socketpool
import wifi

from adafruit_httpserver import Server, Request, Response, Basic, Token, Bearer


# Create a list of available authentication methods.
auths = [
    Basic("user", "password"),
    Token("2db53340-4f9c-4f70-9037-d25bee77eca6"),
    Bearer("642ec696-2a79-4d60-be3a-7c9a3164d766"),
]

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)
server.require_authentication(auths)


@server.route("/implicit-require")
def implicit_require_authentication(request: Request):
    """
    Implicitly require authentication because of the server.require_authentication() call.
    """

    return Response(request, body="Authenticated", content_type="text/plain")


server.serve_forever(str(wifi.radio.ipv4_address))
