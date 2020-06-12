import os

from flask import Flask

# This archive serves double duty: it will contain the application factory, 
# and it tells Python that the flaskr directory should be treated as a package.

# create_app is the application factory function.
def create_app(test_config=None):
    # create and configure the app.
    app = Flask(__name__, instance_relative_config=True)
    # __name__ is the name of the current Python module.
    # The app needs to know where it’s located to set up some paths, 
    # and __name__ is a convenient way to tell it that.

    # instance_relative_config=True tells the app that configuration files are relative 
    # to the instance folder.
    # The instance folder is located outside the flaskr package and can hold local data 
    # that shouldn’t be committed to version control, such as configuration secrets and the database file.
    app.config.from_mapping(
        # sets some default configuration that the app will use:
        SECRET_KEY = 'dev',
        # SECRET_KEY is used by Flask and extensions to keep data safe.
        # It should be overridden with a random value when deploying.
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite'),
        # DATABASE is the path where the SQLite database file will be saved.
    )

    if test_config is None:
        # Load the test config, if exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
        # overrides the default configuration with values taken from the config.py 
        # file in the instance folder if it exists. For example, when deploying, 
        # this can be used to set a real SECRET_KEY.
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)
        # test_config can also be passed to the factory, 
        # and will be used instead of the instance configuration.

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
        # os.makedirs() ensures that app.instance_path exists. 
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    # @app.route() creates a simple route so you can see the application working.
    def hello():
        return 'Hello, World!!!!'

    from . import db
    db.init_app(app)
    # Import and call db function from the factory.

    from . import auth
    app.register_blueprint(auth.bp)
    # Import and register the blueprint from the factory.

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    # Import and register the blueprint of blog.
    # Unlike the auth blueprint, the blog blueprint does not have a url_prefix. 
    # So the index view will be at '/'

    return app

# For Windows cmd, use set instead of export:
# set FLASK_APP=flaskr
# set FLASK_ENV=development
# flask run

# For Windows PowerShell, use $env: instead of export:
# $env:FLASK_APP = "flaskr"
# $env:FLASK_ENV = "development"
# flask run