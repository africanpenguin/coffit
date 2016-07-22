"""Utilities for Coffit."""

from functools import partial


class Namespace(object):
    """Wrapper class for SocketIO.Server"""

    override_methods = ('on', 'emit', 'connect', 'disconnect', 'enter_room')

    def __init__(self, sio, namespace):
        self.sio = sio
        self.namespace = namespace

    def __getattr__(self, name):
        """We override this, """
        if name in self.override_methods:
            return partial(getattr(self.sio, name), namespace=self.namespace)
        else:
            return self.sio.__getattr__(name)


def socketio_namespace(sio, namespace='/'):
    """Return 'namespaced' SocketIO Server object."""
    methods_names = ('on', 'emit', 'disconnect')
    for method_name in methods_names:
        sio_method = getattr(sio, method_name)
        sio_method = (sio_method.func if isinstance(sio_method, partial)
                      else sio_method)
        setattr(sio, method_name, partial(sio_method, namespace=namespace))
    return sio
