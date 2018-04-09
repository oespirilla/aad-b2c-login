
"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, redirect, url_for, session, request, jsonify
from flask_oauthlib.client import OAuth

from home import app, oauth


microsoft = oauth.remote_app(
	'microsoft',
	consumer_key='8600e3dd-ca50-4abd-b1aa-d53ddfdb2cfb',
	consumer_secret='xxxxxxxxxxx',
	request_token_params={'scope': 'offline_access User.Read'},
	base_url='https://graph.microsoft.com/v1.0/',
	request_token_url=None,
	access_token_method='POST',
	access_token_url='https://login.microsoftonline.com/common/oauth2/v2.0/token',
	authorize_url='https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
)


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home',
        year=datetime.now().year
    )

@app.route('/login', methods = ['POST', 'GET'])
def login():
	return microsoft.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('aad_token', None)
    return redirect(url_for('home'))

@app.route('/login/authorized')
def authorized():

    response = microsoft.authorized_response()
    if response is None or response.get('access_token') is None:
        return "Access Denied: Reason=%s\nError=%s" % (response.get('error'),request.get('error_description'))

    session['aad_token'] = (response['access_token'], '')

    return redirect(url_for('home'))

@microsoft.tokengetter
def get_oauth_token():
    return session.get('aad_token')

@app.route('/me')
def me():
	me = microsoft.get('me')
	return str(me.data)