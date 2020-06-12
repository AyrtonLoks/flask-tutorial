# This creates a Blueprint named 'auth'. 
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')
# Like the application object, the blueprint needs to know where it’s defined, 
# so __name__ is passed as the second argument. The url_prefix will be prepended to all the URLs 
# associated with the blueprint.

@bp.route('/register', methods=('GET', 'POST'))
# @bp.route associates the URL /register with the register view function. 
# When Flask receives a request to /auth/register, it will call the register view and 
# use the return value as the response.
def register():
    if request.method == 'POST':
        # If the user submitted the form, request.method will be 'POST'. 
        # In this case, start validating the input
        username = request.form['username']
        password = request.form['password']
        # request.form is a special type of dict mapping submitted form keys and values.
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
        # fetchone() returns one row from the query. If the query returned no results, it returns None.
            error = 'User {} is already registered.'.format(username)
            # Later, fetchall() is used, which returns a list of all results.
        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
                # generate_password_hash() is used to securely hash the password, and that hash is stored.
            )
            db.commit()
            return redirect(url_for('auth.login'))
            # After storing the user, they are redirected to the login page. 
            # url_for() generates the URL for the login view based on its name.
            # redirect() generates a redirect response to the generated URL.

        flash(error)
        # If validation fails, the error is shown to the user.

    return render_template('auth/register.html')
    # render_template() will render a template containing the HTML.

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        # The user is queried first and stored in a variable for later use.

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            # check_password_hash() hashes the submitted password in the same way as 
            # the stored hash and securely compares them.
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            # session is a dict that stores data across requests.
            session['user_id'] = user['id']
            # When validation succeeds, the user’s id is stored in a new session. 
            # The data is stored in a cookie that is sent to the browser, 
            # and the browser then sends it back with subsequent requests. 
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
# bp.before_app_request() registers a function that runs before the view function, 
# no matter what URL is requested.
def load_logged_in_user():
    # load_logged_in_user checks if a user id is stored in the session and gets 
    # that user’s data from the database, storing it on g.user,
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
        # If there is no user id, or if the id doesn’t exist, g.user will be None.
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    # Creating, editing, and deleting blog posts will require a user to be logged in.
    # The new function checks if a user is loaded and redirects to the login page otherwise.
    # If a user is loaded the original view is called and continues normally.
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
            # The url_for() function generates the URL to a view based on a name and arguments.

        return view(**kwargs)

    return wrapped_view
