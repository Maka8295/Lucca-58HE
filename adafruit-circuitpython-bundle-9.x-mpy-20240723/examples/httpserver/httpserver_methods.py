# SPDX-FileCopyrightText: 2023 Michał Pokusa
#
# SPDX-License-Identifier: Unlicense

import socketpool
import wifi

from adafruit_httpserver import Server, Request, JSONResponse, GET, POST, PUT, DELETE


pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, debug=True)

objects = [
    {"id": 1, "name": "Object 1"},
]


@server.route("/api", [GET, POST, PUT, DELETE], append_slash=True)
def api(request: Request):
    """
    Performs different operations depending on the HTTP method.
    """

    # Get objects
    if request.method == GET:
        return JSONResponse(request, objects)

    # Upload or update objects
    if request.method in [POST, PUT]:
        uploaded_object = request.json()

        # Find object with same ID
        for i, obj in enumerate(objects):
            if obj["id"] == uploaded_object["id"]:
                objects[i] = uploaded_object

                return JSONResponse(
                    request, {"message": "Object updated", "object": uploaded_object}
                )

        # If not found, add it
        objects.append(uploaded_object)
        return JSONResponse(
            request, {"message": "Object added", "object": uploaded_object}
        )

    # Delete objects
    if request.method == DELETE:
        deleted_object = request.json()

        # Find object with same ID
        for i, obj in enumerate(objects):
            if obj["id"] == deleted_object["id"]:
                del objects[i]

                return JSONResponse(
                    request, {"message": "Object deleted", "object": deleted_object}
                )

        # If not found, return error
        return JSONResponse(
            request, {"message": "Object not found", "object": deleted_object}
        )

    # If we get here, something went wrong
    return JSONResponse(request, {"message": "Something went wrong"})


server.serve_forever(str(wifi.radio.ipv4_address))
