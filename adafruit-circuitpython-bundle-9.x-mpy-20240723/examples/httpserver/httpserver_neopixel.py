# SPDX-FileCopyrightText: 2022 Michał Pokusa
#
# SPDX-License-Identifier: Unlicense

import board
import neopixel
import socketpool
import wifi

from adafruit_httpserver import Server, Route, as_route, Request, Response, GET, POST


pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)


# This is the simplest way to register a route. It uses the Server object in current scope.
@server.route("/change-neopixel-color", GET)
def change_neopixel_color_handler_query_params(request: Request):
    """Changes the color of the built-in NeoPixel using query/GET params."""

    # e.g. /change-neopixel-color?r=255&g=0&b=0

    r = request.query_params.get("r") or 0
    g = request.query_params.get("g") or 0
    b = request.query_params.get("b") or 0

    pixel.fill((int(r), int(g), int(b)))

    return Response(request, f"Changed NeoPixel to color ({r}, {g}, {b})")


# This is another way to register a route. It uses the decorator that converts the function into
# a Route object that can be imported and registered later.
@as_route("/change-neopixel-color/form-data", POST)
def change_neopixel_color_handler_post_form_data(request: Request):
    """Changes the color of the built-in NeoPixel using POST form data."""

    data = request.form_data  # e.g. r=255&g=0&b=0 or r=255\r\nb=0\r\ng=0
    r, g, b = data.get("r", 0), data.get("g", 0), data.get("b", 0)

    pixel.fill((int(r), int(g), int(b)))

    return Response(request, f"Changed NeoPixel to color ({r}, {g}, {b})")


def change_neopixel_color_handler_post_json(request: Request):
    """Changes the color of the built-in NeoPixel using JSON POST body."""

    data = request.json()  # e.g {"r": 255, "g": 0, "b": 0}
    r, g, b = data.get("r", 0), data.get("g", 0), data.get("b", 0)

    pixel.fill((r, g, b))

    return Response(request, f"Changed NeoPixel to color ({r}, {g}, {b})")


# You can always manually create a Route object and import or register it later.
# Using this approach you can also use the same handler for multiple routes.
post_json_route = Route(
    "/change-neopixel-color/json", POST, change_neopixel_color_handler_post_json
)


def change_neopixel_color_handler_url_params(
    request: Request, r: str = "0", g: str = "0", b: str = "0"
):
    """Changes the color of the built-in NeoPixel using URL params."""

    # e.g. /change-neopixel-color/255/0/0

    pixel.fill((int(r), int(g), int(b)))

    return Response(request, f"Changed NeoPixel to color ({r}, {g}, {b})")


# Registering Route objects
server.add_routes(
    [
        change_neopixel_color_handler_post_form_data,
        post_json_route,
        # You can also register a inline created Route object
        Route(
            path="/change-neopixel-color/<r>/<g>/<b>",
            methods=GET,
            handler=change_neopixel_color_handler_url_params,
        ),
    ]
)


server.serve_forever(str(wifi.radio.ipv4_address))
