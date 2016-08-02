import os


class EnvConfig(object):
    """Config that checks os.environ first."""

    APP_NAME = __name__
    DATABASE_URL = 'sqlite:///coffit.db'
    CONNECTED_ROOM = 'coffee_lounge'
    JWT_SECRET = 'secret'
    SERVER_PORT = 5000

    def __getattribute__(self, name):
        return os.environ.get(name, object.__getattribute__(self, name))

config = EnvConfig()
