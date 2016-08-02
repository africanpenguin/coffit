"""Socket."""

from __future__ import absolute_import, print_function

import socketio

sio = socketio.Server()

app = socketio.Middleware(sio)
