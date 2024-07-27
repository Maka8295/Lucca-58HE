# SPDX-FileCopyrightText: 2023 Michał Pokusa
#
# SPDX-License-Identifier: Unlicense

import socketpool
import wifi

from adafruit_httpserver import Server, Request, Response, GET, POST


pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, debug=True)


FORM_HTML_TEMPLATE = """
<html lang="en">
    <head>
        <title>Form with {enctype} enctype</title>
    </head>
    <body>
        <a href="/form?enctype=application/x-www-form-urlencoded">
            <button>Load <strong>application/x-www-form-urlencoded</strong> form</button>
        </a><br />
        <a href="/form?enctype=multipart/form-data">
            <button>Load <strong>multipart/form-data</strong> form</button>
        </a><br />
        <a href="/form?enctype=text/plain">
            <button>Load <strong>text/plain</strong> form</button>
        </a><br />

        <h2>Form with {enctype} enctype</h2>
        <form action="/form" method="post" enctype="{enctype}">
            <input type="text" name="something" placeholder="Type something...">
            <input type="submit" value="Submit">
        </form>
        {submitted_value}
    </body>
</html>
"""


@server.route("/form", [GET, POST])
def form(request: Request):
    """
    Serve a form with the given enctype, and display back the submitted value.
    """
    enctype = request.query_params.get("enctype", "text/plain")

    if request.method == POST:
        posted_value = request.form_data.get("something")

    return Response(
        request,
        FORM_HTML_TEMPLATE.format(
            enctype=enctype,
            submitted_value=(
                f"<h3>Enctype: {enctype}</h3>\n<h3>Submitted form value: {posted_value}</h3>"
                if request.method == POST
                else ""
            ),
        ),
        content_type="text/html",
    )


server.serve_forever(str(wifi.radio.ipv4_address))
