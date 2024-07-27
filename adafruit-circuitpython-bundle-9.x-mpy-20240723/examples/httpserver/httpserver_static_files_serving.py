# SPDX-FileCopyrightText: 2023 Michał Pokusa
#
# SPDX-License-Identifier: Unlicense


import socketpool
import wifi

from adafruit_httpserver import Server, MIMETypes


MIMETypes.configure(
    default_to="text/plain",
    # Unregistering unnecessary MIME types can save memory
    keep_for=[".html", ".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".ico"],
    # If you need to, you can add additional MIME types
    register={".foo": "text/foo", ".bar": "text/bar"},
)

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)

# You don't have to add any routes, by default the server will serve files
# from it's root_path, which is set to "/static" in this example.

# If you don't set a root_path, the server will not serve any files.

server.serve_forever(str(wifi.radio.ipv4_address))
