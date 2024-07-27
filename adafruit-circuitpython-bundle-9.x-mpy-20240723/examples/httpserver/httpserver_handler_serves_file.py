# SPDX-FileCopyrightText: 2022 Dan Halbert for Adafruit Industries, Michał Pokusa
#
# SPDX-License-Identifier: Unlicense


import socketpool
import wifi

from adafruit_httpserver import Server, Request, FileResponse


pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/default-static-folder", debug=True)


@server.route("/home")
def home(request: Request):
    """
    Serves the file /other-static-folder/home.html.
    """

    return FileResponse(request, "home.html", "/other-static-folder")


server.serve_forever(str(wifi.radio.ipv4_address))
