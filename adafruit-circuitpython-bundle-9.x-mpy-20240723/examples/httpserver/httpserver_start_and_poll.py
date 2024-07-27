# SPDX-FileCopyrightText: 2022 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import socketpool
import wifi

from adafruit_httpserver import (
    Server,
    REQUEST_HANDLED_RESPONSE_SENT,
    Request,
    FileResponse,
)


pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)


@server.route("/")
def base(request: Request):
    """
    Serve the default index.html file.
    """
    return FileResponse(request, "index.html")


# Start the server.
server.start(str(wifi.radio.ipv4_address))

while True:
    try:
        # Do something useful in this section,
        # for example read a sensor and capture an average,
        # or a running total of the last 10 samples

        # Process any waiting requests
        pool_result = server.poll()

        if pool_result == REQUEST_HANDLED_RESPONSE_SENT:
            # Do something only after handling a request
            pass

        # If you want you can stop the server by calling server.stop() anywhere in your code
    except OSError as error:
        print(error)
        continue
