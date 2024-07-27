# SPDX-FileCopyrightText: 2023 Michał Pokusa
#
# SPDX-License-Identifier: Unlicense

from time import monotonic
import microcontroller
import socketpool
import wifi

from adafruit_httpserver import Server, Request, Response, SSEResponse, GET


pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, debug=True)


sse_response: SSEResponse = None
next_event_time = monotonic()

HTML_TEMPLATE = """
<html lang="en">
    <head>
        <title>Server-Sent Events Client</title>
    </head>
    <body>
        <p>CPU temperature: <strong>-</strong>&deg;C</p>
        <script>
            const eventSource = new EventSource('/connect-client');
            const cpuTemp = document.querySelector('strong');

            eventSource.onmessage = event => cpuTemp.textContent = event.data;
            eventSource.onerror = error => cpuTemp.textContent = error;
        </script>
    </body>
</html>
"""


@server.route("/client", GET)
def client(request: Request):
    return Response(request, HTML_TEMPLATE, content_type="text/html")


@server.route("/connect-client", GET)
def connect_client(request: Request):
    global sse_response  # pylint: disable=global-statement

    if sse_response is not None:
        sse_response.close()  # Close any existing connection

    sse_response = SSEResponse(request)

    return sse_response


server.start(str(wifi.radio.ipv4_address))
while True:
    server.poll()

    # Send an event every second
    if sse_response is not None and next_event_time < monotonic():
        cpu_temp = round(microcontroller.cpu.temperature, 2)
        sse_response.send_event(str(cpu_temp))
        next_event_time = monotonic() + 1
