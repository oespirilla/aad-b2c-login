"""
The flask application package.
"""

from flask import Flask
from flask_oauthlib.client import OAuth
app = Flask(__name__)
app.debug = True
app.secret_key = '4b34b1c1d1a2f41ea9564c483311fbd9d07bc704b164ea2d'
oauth = OAuth(app)

import home.main