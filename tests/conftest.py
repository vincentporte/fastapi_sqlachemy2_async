import asyncio
from contextlib import ExitStack

import pytest
from fastapi.testclient import TestClient
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor

from app.main import MainApp
from app.services.database import get_db, sessionmanager

test_db = factories.postgresql_proc(port=None, dbname="test_db")


@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        yield MainApp(init_db=False).app


@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c


# create a new session-scoped event loop fixture, because
# the default event loop fixture is function-scoped
@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# test connection will be scoped to the session, so that we can use
# the same connection for all the tests, as it's best practice
# to avoid creating a new connection for each test, or even request
@pytest.fixture(scope="session", autouse=True)
async def connection_test(test_db, event_loop):
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_db = test_db.dbname
    pg_password = test_db.password

    # The DatabaseJanitor manages the state of the database, but we need to create
    # the connection ande session. Here we're initializing our sessionmanager singleton
    # with the connection settings provided by the postgresql_proc fixture. After our tests
    # are finished, we'll call the close method to dispose our async database engine.
    with DatabaseJanitor(pg_user, pg_host, pg_port, pg_db, test_db.version, pg_password):
        connection_str = f"postgresql+psycopg://{pg_user}:@{pg_host}:{pg_port}/{pg_db}"
        sessionmanager.init(connection_str)
        yield
        await sessionmanager.close()


# function-scoped fixture that will handle creating the database session for each test
#
# Here we're creating the database tables from scratch for each test. Having this done
# in an isolated connection will ensure that these operations are finished before our tests run.
# We also don't have to bother with cleaning up the database after the tests are done,
# because the DatabaseJanitor will take care of that for us.
#
# We're also overriding the get_db FastAPI dependency we've created earlier with a new dependency
# that will return our test session. Notice that, as was the case with the original get_db dependency,
# this will ensure that each time we call a FastAPI endpoint, we'll be using a new isolated session
@pytest.fixture(scope="function", autouse=True)
async def create_tables(connection_test):
    async with sessionmanager.connect() as connection:
        await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection)


@pytest.fixture(scope="function", autouse=True)
async def db_session():
    async with sessionmanager.session() as session:
        yield session


@pytest.fixture(scope="function", autouse=True)
async def session_override(app, connection_test):
    app.dependency_overrides[get_db] = db_session
