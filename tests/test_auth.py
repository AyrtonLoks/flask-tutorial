import pytest
from flask import g, session
from flaskr.db import get_db


# The register view should render successfully on GET. On POST with valid form data, 
# it should redirect to the login URL and the user’s data should be in the database. 
# Invalid data should display error messages.
def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    # client.get() makes a GET request and returns the Response object returned by Flask. 
    # Similarly, client.post() makes a POST request, converting the data dict into form data
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )
    assert 'http://localhost/auth/login' == response.headers['Location']
    # headers will have a Location header with the login URL when the register view redirects 
    # to the login view.

    with app.app_context():
        assert get_db().execute(
            "select * from user where username = 'a'",
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
        # data contains the body of the response as bytes.
        # If you want to compare Unicode text, use get_data(as_text=True) instead.
    )
    assert message in response.data

def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'
        # Using client in a with block allows accessing context variables such as session 
        # after the response is returned.

# pytest.mark.parametrize tells Pytest to run the same test function with different arguments.
@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data

# Testing logout is the opposite of login. session should not contain user_id after logging out.
def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session