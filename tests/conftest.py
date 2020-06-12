import os
import tempfile
import pytest

from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

# The app fixture will call the factory and pass test_config to configure the application 
# and database for testing instead of using your local development configuration.
@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    # tempfile.mkstemp() creates and opens a temporary file, returning the file object and the path to it.
    app = create_app({
        'TESTING': True,
        # TESTING tells Flask that the app is in test mode.
        'DATABASE': db_path,
        # The DATABASE path is overridden so it points to this temporary path 
        # instead of the instance folder.
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    # The client fixture calls app.test_client() with the application object created by the app fixture. 
    # Tests will use the client to make requests to the application without running the server.
    return app.test_client()


@pytest.fixture
def runner(app):
    # The runner fixture is similar to client. app.test_cli_runner() creates a runner that 
    # can call the Click commands registered with the application.
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')

# With the auth fixture, you can call auth.login() in a test to log in as the test user, 
# which was inserted as part of the test data in the app fixture.
@pytest.fixture
def auth(client):
    return AuthActions(client)
