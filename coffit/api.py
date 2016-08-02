from __future__ import absolute_import, print_function

from .socket import sio

from .utils import Namespace
from .config import config
from .auth import verify_token

api = Namespace(sio, '/')


@api.on('connect')
def connect(sid, environ):
    print('[main] connect ', sid)


@api.on('join_room')
def join_room(sid, data):
    token = data.get('access_token')
    if token:
        user = verify_token(token)['username']
        print('[main] Token valid. {user} joined the room!'.format(user=user))

        api.enter_room(sid, room=config.CONNECTED_ROOM)
        welcome = 'Welcome to the room {user}'.format(user=user['user'])
        sio.emit('my response', data=welcome, room=config.CONNECTED_ROOM)


@api.on('my message')
def message(sid, data):
    print('[main] Received message ', data)
    api.emit('my response', {'data': 'Received message: ' + data['data']},
             room=sid)


@api.on('disconnect')
def disconnect(sid):
    print('[main] disconnect ', sid)
