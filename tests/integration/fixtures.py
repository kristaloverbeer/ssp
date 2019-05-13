import os

import psycopg2
import pytest
from pytest_postgresql.factories import drop_postgresql_database

from src.database.models import db as _db
from src.server import api


@pytest.fixture(scope='session')
def database(request):
    _init_postgres_database()

    @request.addfinalizer
    def drop_database():
        drop_postgresql_database(
                os.environ.get('POSTGRES_USER'),
                os.environ.get('POSTGRES_HOST'),
                os.environ.get('POSTGRES_PORT'),
                os.environ.get('POSTGRES_DB'),
                9.6,
            )


@pytest.fixture(scope='session')
def app(request, database):
    ctx = api.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)

    return api


@pytest.fixture(scope='function')
def db(app, request):
    _db.app = app
    _db.create_all()

    def teardown():
        _db.drop_all()

    request.addfinalizer(teardown)

    return _db


@pytest.fixture(scope='function')
def db_session(db, request):
    connection = _db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = _db.create_scoped_session(options=options)

    _db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


def _init_postgres_database():
    user = os.environ.get('POSTGRES_USER')
    host = os.environ.get('POSTGRES_HOST')
    port = os.environ.get('POSTGRES_PORT')
    db_name = os.environ.get('POSTGRES_DB')

    conn = psycopg2.connect(user=user, host=host, port=port)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute('CREATE DATABASE "{0}";'.format(db_name))

    cur.close()
    conn.close()
