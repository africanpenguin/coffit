"""Namespace that handles user authentication."""

from datetime import datetime, timedelta
import jwt
from jwt.exceptions import InvalidTokenError

from . import sio
from .config import config
from .utils import Namespace

auth = Namespace(sio, '/auth')


# FIXME: Add proper database model...
users = {
    'admin': {
        'id': '1',
        'username': 'admin',
        'password': 'admin'
    },
    'coffit': {
        'id': '2',
        'username': 'coffit',
        'password': 'coffit'
    },
    'test': {
        'id': '3',
        'username': 'test',
        'password': 'test'
    },
}

users_by_id = {u['id']: u for u in users.values()}


@auth.on('connect')
def connect(sid, environ):
    print('[/auth] connect ', sid)


@auth.on('disconnect')
def disconnect(sid):
    print('[/auth] disconnect ', sid)


@auth.on('login')
def login(sid, data):
    username = data.get('user')
    password = data.get('pass')
    if users.get(username, {}).get('password') == password:
        print('[/auth] succesfull login for {user}!'.format(user=username))

        # Return a valid JWT
        token = generate_token(users[username]['id'])
        auth.emit('login_success', data={'access_token': token}, room=sid)


def generate_token(user_id):
    """Generates a token from """
    expiry_timestamp = datetime.utcnow() + timedelta(days=60)
    payload = dict(user=user_id,
                   iss=config.APP_NAME,
                   exp=expiry_timestamp)
    return jwt.encode(payload=payload,
                      key=config.JWT_SECRET,
                      algorithm='HS512')


def verify_token(token):
    try:
        data = jwt.decode(token, key=config.JWT_SECRET, algorithms=['HS512'])
        user_id = data.get('id')
        return users_by_id.get(user_id)
    except InvalidTokenError:
        return False
