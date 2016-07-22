from setuptools import setup

# FIXME: Add versions to dependencies...
extras_require = {
    'tests': [
        'pytest',
        'mock',
    ],
    'postgres': [
        'psycopg2',
    ]
}
extras_require['all'] = list({r for e in extras_require.values() for r in e})

install_requires = [
    'click',
    'gevent',
    'gevent-websocket',
    'greenlet',
    'gunicorn',
    'ipython',
    'marshmallow-sqlalchemy',
    'pyjwt',
    'pysqlite',
    'python-engineio',
    'python-socketio',
    'sqlalchemy',
    'sqlalchemy-utils[enum,password]',
]

setup(
    name='coffit',
    version='0.1.0.dev',
    description='CoffIT Backend App',
    long_description=open('README.md').read(),
    install_requires=install_requires,
    extras_require=extras_require,
    packages=['coffit'],
    entry_points={
        'console_scripts': [
            'coffit = coffit.cli:cli',
        ],
    },
    zip_safe=False,
)
