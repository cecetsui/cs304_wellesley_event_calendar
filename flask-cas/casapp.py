#!/usr/local/bin/python2.7

from flask import (Flask, render_template, make_response, request, redirect, url_for,
                   session, flash, send_from_directory)
from werkzeug import secure_filename
# new
from flask_cas import CAS

app = Flask(__name__)
app.secret_key = 'rosebud'

CAS(app)
app.config['CAS_SERVER'] = 'https://login.wellesley.edu:443'
app.config['CAS_AFTER_LOGIN'] = 'logged_in'
app.config['CAS_LOGIN_ROUTE'] = '/module.php/casserver/cas.php/login'
app.config['CAS_LOGOUT_ROUTE'] = '/module.php/casserver/cas.php/logout'
# app.config['CAS_AFTER_LOGOUT'] = 'http://cs.wellesley.edu:1942/'
app.config['CAS_AFTER_LOGOUT'] = 'https://cs.wellesley.edu:1942/scott'
app.config['CAS_VALIDATE_ROUTE'] = '/module.php/casserver/serviceValidate.php'

import os
import imghdr

app.secret_key = 'rosebud'

@app.route('/logged_in/')
def logged_in():
    flash('successfully logged in!')
    return redirect( url_for('index') )

@app.route('/')
def index():
    print session.keys()
    for k in session.keys():
        print k,' => ',session[k]
    if '_CAS_TOKEN' in session:
        token = session['_CAS_TOKEN']
    if 'CAS_ATTRIBUTES' in session:
        attribs = session['CAS_ATTRIBUTES']
        for k in attribs:
            print k,' => ',attribs[k]
    if 'CAS_USERNAME' in session:
        is_logged_in = True
        username = session['CAS_USERNAME']
    else:
        is_logged_in = False
        username = None
    return render_template('main.html', username=username, is_logged_in=is_logged_in)


@app.route('/scott/')
def logged_out():
    flash('successfully logged out!')
    return redirect( url_for('index') )



if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', 1234)
