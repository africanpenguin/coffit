import socketio

sio = socketio.Server()

from . import models  # noqa
from . import api, auth  # noqa

app = socketio.Middleware(sio)
