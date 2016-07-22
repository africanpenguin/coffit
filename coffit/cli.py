import click
from sqlalchemy_utils import create_database, database_exists, drop_database

from .config import config
from .models import Base, engine


#
# Database
#
@click.group()
def db():
    """Database management."""
    pass


@db.command('init')
@click.option('--url', default=config.DATABASE_URL,
              help=('Database URL. '
                    'eg. "postgresql+psycopg2://user:pass@localhost/coffit"'))
def init_db(url):
    if database_exists(url):
        click.secho('Database %s already exists...' % url, fg='yellow')
        click.confirm('Drop and create new?', default=False, abort=True)
        click.secho('Dropping %s...' % url, fg='red')
        drop_database(url)
    click.secho('Creating %s...' % url, fg='blue')
    create_database(url)
    click.secho('Creating tables...', fg='blue')
    Base.metadata.create_all(engine)
    click.secho('Database initialized!', fg='green')


@click.group()
def cli():
    """CoffIT CLI management."""
    pass


@cli.command()
def run():
    """"""
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
    server = WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()


cli.add_command(db)


if __name__ == '__main__':
    cli()
