from __future__ import absolute_import, print_function

import click
from sqlalchemy_utils import create_database, database_exists, drop_database

from .config import config
from .models import Base, engine


def abort_if_false(ctx, param, value):
    """Abort command is value is False."""
    if not value:
        ctx.abort()


#
# Database
#
@click.group()
def db():
    """Database management."""
    pass


@db.command('init')
@click.pass_context
def db_init(ctx):
    """Create db."""
    url = config.DATABASE_URL
    if database_exists(url):
        click.secho('Database %s already exists...' % url, fg='yellow')
        ctx.abort()
    click.secho('Creating %s...' % url, fg='blue')
    create_database(url)
    click.secho('Creating tables...', fg='blue')
    Base.metadata.create_all(engine)
    click.secho('Database initialized!', fg='green')


@db.command('drop')
@click.option('--yes-i-know', is_flag=True, expose_value=False,
              callback=abort_if_false,
              prompt='Are you sure you want to drop the db?')
def db_drop():
    """Drop db."""
    url = config.DATABASE_URL
    click.secho('Dropping %s...' % url, fg='red')
    if database_exists(url):
        drop_database(url)


@click.group()
def cli():
    """CoffIT CLI management."""
    pass


@click.group()
def server():
    """Server CLI."""
    pass


@server.command()
def run():
    """Run coffit."""
    click.secho('Running CoffIT server...', fg='blue')
    click.secho('Note: This instance also serves "examples/index.html" for '
                'testing purposes.', fg='yellow')

    from . import sio
    from socketio import Middleware
    from gevent.pywsgi import WSGIServer
    from geventwebsocket.handler import WebSocketHandler

    def static_wsgi_app(environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return open('examples/index.html', 'rb').read()

    app = Middleware(sio, wsgi_app=static_wsgi_app)
    server = WSGIServer(('', config.SERVER_PORT), app,
                        handler_class=WebSocketHandler)
    server.serve_forever()


cli.add_command(db)
cli.add_command(server)
