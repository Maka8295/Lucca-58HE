# SPDX-FileCopyrightText: 2022 Michał Pokusa
#
# SPDX-License-Identifier: Unlicense

import mdns
import socketpool
import wifi

from adafruit_httpserver import Server, Request, FileResponse


mdns_server = mdns.Server(wifi.radio)
mdns_server.hostname = "custom-mdns-hostname"
mdns_server.advertise_service(service_type="_http", protocol="_tcp", port=5000)

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)


@server.route("/")
def base(request: Request):
    """
    Serve the default index.html file.
    """

    return FileResponse(request, "index.html", "/www")


server.serve_forever(str(wifi.radio.ipv4_address))
