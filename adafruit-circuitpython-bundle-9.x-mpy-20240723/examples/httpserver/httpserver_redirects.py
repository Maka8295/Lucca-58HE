# SPDX-FileCopyrightText: 2023 Michał Pokusa
#
# SPDX-License-Identifier: Unlicense

import socketpool
import wifi

from adafruit_httpserver import (
    Server,
    Request,
    Response,
    Redirect,
    POST,
    NOT_FOUND_404,
    MOVED_PERMANENTLY_301,
)


pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, debug=True)

REDIRECTS = {
    "google": "https://www.google.com",
    "adafruit": "https://www.adafruit.com",
    "circuitpython": "https://circuitpython.org",
}


@server.route("/blinka")
def redirect_blinka(request: Request):
    """Always redirect to a Blinka page as permanent redirect."""
    return Redirect(request, "https://circuitpython.org/blinka", permanent=True)


@server.route("/adafruit")
def redirect_adafruit(request: Request):
    """Permanent redirect to Adafruit website with explicitly set status code."""
    return Redirect(request, "https://www.adafruit.com/", status=MOVED_PERMANENTLY_301)


@server.route("/fake-login", POST)
def fake_login(request: Request):
    """Fake login page."""
    return Response(request, "Fake login page with POST data preserved.")


@server.route("/login", POST)
def temporary_login_redirect(request: Request):
    """Temporary moved login page with preserved POST data."""
    return Redirect(request, "/fake-login", preserve_method=True)


@server.route("/<slug>")
def redirect_other(request: Request, slug: str = None):
    """
    Redirect to a URL based on the slug.
    """

    if slug is None or slug not in REDIRECTS:
        return Response(request, "Unknown redirect", status=NOT_FOUND_404)

    return Redirect(request, REDIRECTS.get(slug))


server.serve_forever(str(wifi.radio.ipv4_address))
