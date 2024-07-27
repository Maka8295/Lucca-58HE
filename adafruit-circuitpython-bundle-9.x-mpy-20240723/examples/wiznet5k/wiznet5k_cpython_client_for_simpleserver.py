# SPDX-FileCopyrightText: 2023 ladyada
#
# SPDX-License-Identifier: MIT
#!/usr/bin/env python3

"""
This example client runs on CPython and connects to / sends data to the
simpleserver example.
"""
import socket
import time

print("A simple client for the wiznet5k_simpleserver.py example in this directory")
print(
    "Run this on any device connected to the same network as the server, after "
    "editing this script with the correct HOST & PORT\n"
)
# Or, use any TCP-based client that can easily send 1024 bytes. For example:
#     python -c 'print("1234"*256)' | nc 192.168.10.1 50007


# edit host and port to match server
HOST = "192.168.10.1"
PORT = 50007
TIMEOUT = 10
INTERVAL = 5
MAXBUF = 1024

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(TIMEOUT)
    print(f"Connecting to {HOST}:{PORT}")
    s.connect((HOST, PORT))
    # wiznet5k_simpleserver.py wants exactly 1024 bytes
    size = s.send(b"A5" * 512)
    print("Sent", size, "bytes")
    buf = s.recv(MAXBUF)
    print("Received", buf)
    s.close()
    time.sleep(INTERVAL)
