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
        return '头条资讯！'
    else:
        return 'TODO'

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0')

