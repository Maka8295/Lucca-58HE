# SPDX-FileCopyrightText: 2022 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import microcontroller
import socketpool
import wifi

from adafruit_httpserver import Server, Request, JSONResponse


pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, debug=True)

# (Optional) Allow cross-origin requests.
server.headers = {
    "Access-Control-Allow-Origin": "*",
}


@server.route("/cpu-information", append_slash=True)
def cpu_information_handler(request: Request):
    """
    Return the current CPU temperature, frequency, and voltage as JSON.
    """

    data = {
        "temperature": microcontroller.cpu.temperature,
        "frequency": microcontroller.cpu.frequency,
        "voltage": microcontroller.cpu.voltage,
    }

    return JSONResponse(request, data)


server.serve_forever(str(wifi.radio.ipv4_address))
