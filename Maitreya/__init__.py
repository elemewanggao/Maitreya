# -*- coding:utf-8 -*-
"""app入口，用gunicorn直接启动."""

from flask import Flask
from gevent import monkey
from flask_cors import CORS
from .settings import CORS_CONF


app = Flask(__name__)
CORS(app, resources=CORS_CONF, supports_credentials=True)
monkey.patch_all()


@app.route('/')
def hi_maitreya():
    """你好，我的弥勒佛"""
    return 'hi maitreya!'
