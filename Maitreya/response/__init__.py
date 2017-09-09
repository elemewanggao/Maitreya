# -*- coding:utf-8 -*-
from flask import make_response, Response
from werkzeug.wrappers import Response as wResponse
from Maitreya.exception import MaitreyaCustomExc
from Maitreya.log import get_logger
import jsonpickle


logger = get_logger(__name__)


def make_res(obj):
    """将一个对象obj封装成一个response返回."""
    if isinstance(obj, (Response, wResponse)):
        return obj
    else:
        resp_dict = dict(code=200, msg='ok', data=obj)
        return make_response(jsonpickle.encode(resp_dict))


def make_exc_response(exc):
    """返回一个异常response."""
    logger.exception(repr(exc))
    if isinstance(exc, MaitreyaCustomExc):
        return_dict = dict(code=exc.code, msg=exc.msg)
        return make_response(jsonpickle.encode(return_dict), exc.http_code)
    else:
        return_dict = dict(code=501, msg='server error')
        return make_response(jsonpickle.encode(return_dict), 500)
