# SPDX-FileCopyrightText: 2023 Michał Pokusa
#
# SPDX-License-Identifier: Unlicense

from asyncio import create_task, gather, run, sleep as async_sleep
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


async def handle_http_requests():
    while True:
        # Process any waiting requests
        pool_result = server.poll()

        if pool_result == REQUEST_HANDLED_RESPONSE_SENT:
            # Do something only after handling a request
            pass

        await async_sleep(0)


async def do_something_useful():
    while True:
        # Do something useful in this section,
        # for example read a sensor and capture an average,
        # or a running total of the last 10 samples
        await async_sleep(1)

        # If you want you can stop the server by calling server.stop() anywhere in your code


async def main():
    await gather(
        create_task(handle_http_requests()),
        create_task(do_something_useful()),
    )


run(main())
