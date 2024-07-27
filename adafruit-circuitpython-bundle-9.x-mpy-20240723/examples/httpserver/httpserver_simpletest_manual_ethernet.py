# SPDX-FileCopyrightText: 2023 Tim C for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import board
import digitalio

from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K
from adafruit_wiznet5k import adafruit_wiznet5k_socket as socket
from adafruit_httpserver import Server, Request, Response


# For Adafruit Ethernet FeatherWing
cs = digitalio.DigitalInOut(board.D10)

# For Particle Ethernet FeatherWing
# cs = digitalio.DigitalInOut(board.D5)

spi_bus = board.SPI()

# Initialize ethernet interface with DHCP
eth = WIZNET5K(spi_bus, cs)

# Set the interface on the socket source
socket.set_interface(eth)

server = Server(socket, "/static", debug=True)


@server.route("/")
def base(request: Request):
    """
    Serve a default static plain text message.
    """
    return Response(request, "Hello from the CircuitPython HTTP Server!")


server.serve_forever(str(eth.pretty_ip(eth.ip_address)))
