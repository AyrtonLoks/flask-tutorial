from flaskr import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'
# Added the hello route as an example when writing the factory at the beginning of the tutorial. 
# It returns “Hello, World!”, so the test checks that the response data matches.

# To run the tests, use the pytest command. It will find and run all the test functions you’ve written.
# If any tests fail, pytest will show the error that was raised. 
# You can run pytest -v to get a list of each test function rather than dots.

# To measure the code coverage of your tests, use the coverage command to run pytest instead of 
# running it directly: coverage run -m pytest
# You can either view a simple coverage report in the terminal: coverage report

# An HTML report allows you to see which lines were covered in each file: coverage html