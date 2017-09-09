# -*- coding:utf-8 -*-
"""app入口，用gunicorn直接启动."""
import time
import logging.config
from flask import Flask, request
from gevent import monkey
from flask_cors import CORS
from Maitreya.settings import CORS_CONF, LOGGING
from Maitreya.log import get_logger
from Maitreya.utils.decorator import api
from Maitreya.server.test import test


app = Flask(__name__)
CORS(app, resources=CORS_CONF, supports_credentials=True)
monkey.patch_all()

logging.config.dictConfig(LOGGING)
logger = get_logger(__name__)


@app.errorhandler(404)
def not_found_err(error):
    """Not found."""
    return 'not found', 404


@app.errorhandler(500)
def server_err(error):
    """Server error."""
    return 'service exception', 500


@app.route('/test')
@api
def test1():
    return 'test'


@app.before_request
def before_request():
    logger.info('before request, {}:{}=>{}'.format(
        request.method, request.url, request.url_rule))
    request.start_time = time.time()


@app.after_request
def after_request(response):
    timing = (time.time() - request.start_time) * 1000
    logger.info('after request, {}:{}=>{}=>{}:{}'.format(
        request.method, request.url, request.url_rule, response.status_code, timing))
    return response


app.register_blueprint(test)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7008, debug=True)
