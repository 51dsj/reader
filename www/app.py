# !/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from flask import Flask
from flask import (render_template, g, session, redirect, url_for, request, flash)
from flask_bootstrap import Bootstrap

import config
from database import db_session, init_db

app = Flask(__name__)
app.config.from_object(config)
bootstrap = Bootstrap(app)


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('index.html')
    else:
        return 'TODO'


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'GET':
        return 'hello,admin!'
    else:
        return 'TODO'


@app.route('/auth/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        return 'TODO'


@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        return 'TODO'


@app.route('/tech/')
def tech():
    return render_template('tech.html')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0')

