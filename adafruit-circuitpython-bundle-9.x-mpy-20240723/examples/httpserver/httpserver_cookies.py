# SPDX-FileCopyrightText: 2023 Michał Pokusa
#
# SPDX-License-Identifier: Unlicense

import socketpool
import wifi

from adafruit_httpserver import Server, Request, Response, GET, Headers


pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, debug=True)


THEMES = {
    "dark": {
        "background-color": "#1c1c1c",
        "color": "white",
        "button-color": "#181818",
    },
    "light": {
        "background-color": "white",
        "color": "#1c1c1c",
        "button-color": "white",
    },
}


def themed_template(user_preferred_theme: str):
    theme = THEMES[user_preferred_theme]

    return f"""
    <html>
        <head>
            <title>Cookie Example</title>
            <style>
                body {{
                    background-color: {theme['background-color']};
                    color: {theme['color']};
                }}

                button {{
                    background-color: {theme['button-color']};
                    color: {theme['color']};
                    border: 1px solid {theme['color']};
                    padding: 10px;
                    margin: 10px;
                }}
            </style>
        </head>
        <body>
            <a href="/?theme=dark"><button>Dark theme</button></a>
            <a href="/?theme=light"><button>Light theme</button></a>
            <br />
            <p>
                After changing the theme, close the tab and open again.
                Notice that theme stays the same.
            </p>
        </body>
    </html>
    """


@server.route("/", GET)
def themed_from_cookie(request: Request):
    """
    Serve a simple themed page, based on the user's cookie.
    """

    user_theme = request.cookies.get("theme", "light")
    wanted_theme = request.query_params.get("theme", user_theme)

    headers = Headers()
    headers.add("Set-Cookie", "cookie1=value1")
    headers.add("Set-Cookie", "cookie2=value2")

    return Response(
        request,
        themed_template(wanted_theme),
        content_type="text/html",
        headers=headers,
        cookies={} if user_theme == wanted_theme else {"theme": wanted_theme},
    )


server.serve_forever(str(wifi.radio.ipv4_address))
