# -*- coding:utf-8 -*-
import functools
from flask import request
from Maitreya.response import make_exc_response, make_res
from Maitreya.request import get_request_args


def api(func):
    """返回装饰器."""
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        response = None
        try:
            req_params = get_request_args(request)
            kwargs.update(req_params)
            res = func(*args, **kwargs)
        except Exception as e:
            response = make_exc_response(e)
        else:
            response = make_res(res)
        finally:
            response.headers['Content-Type'] = 'application/json'
            return response
    return wrap
