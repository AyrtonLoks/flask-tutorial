from flask import Flask
# Imported the Class Flask, an instance of our application will be our WSGI application.
# WSGI(Web Server Gateway Interface) is provided by Werkzeug, is a simple and universal interface
# between web servers and web applications or frameworks for Python.

app = Flask(__name__)
# 'app' is a instance of the imported class. '__name__' is the first argument, and the name of the
# application's module or pack.
# In a single module, should use '__name__' because depending on if it's started as application or 
# module the name will be different.
# This is needed so that Flask knows where to look for templates, static files, and so on. 

# A Flask application is an instance of the Flask class. Everything about the application, 
# such as configuration and URLs, will be registered with this class.

# Use route() decorator to tell Flask what URL should triger our function.
# The function is given a name which is also used to generate URLs for that particular function, 
# and return the message we want to display in the user's browser.
@app.route('/')
def hello():
    return 'Hello, World!'


# To run the application you can either use the flask command or python’s -m switch with Flask.
# Before you can do that you need to tell your terminal the application to work with by exporting 
# the FLASK_APP environment variable:

#On Command Prompt: set FLASK_APP=hello.py

#on PowerShell: $env:FLASK_APP = "hello.py"

# flask run
#Alternatively you can use python -m flask: python -m flask run