# -*- coding:utf-8 -*-
"""app入口，用gunicorn直接启动."""
import logging.config
from flask import Flask
from gevent import monkey
from flask_cors import CORS
from Maitreya.settings import CORS_CONF, LOGGING
from Maitreya.router import route_init


app = Flask(__name__)
CORS(app, resources=CORS_CONF, supports_credentials=True)
monkey.patch_all()

logging.config.dictConfig(LOGGING)
route_init(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7007, debug=True)
