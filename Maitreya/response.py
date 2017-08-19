#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps
from werkzeug.exceptions import HTTPException
import tempfile

from flask import (
    make_response,
    Response,
    send_file,
)
from werkzeug.wrappers import Response as wResponse

from Maitreya.utils import jsonpickle_dumps
from Maitreya.exception import MaitreyaExc


def make_res(obj):
    """Make a flask response on call ok,
    `obj` is a flask/werkzeug response object that can be jsonified."""
    if isinstance(obj, (Response, wResponse)):
        return obj
    dct = dict(code=200, msg='ok', data=obj)
    return make_response(jsonpickle_dumps(dct))


def make_excel_res(content):
    """返回客户端excel."""
    temp_file = tempfile.TemporaryFile()
    temp_file.write(content)

    temp_file.seek(0)
    response = send_file(temp_file, as_attachment=True,
                         mimetype='application/vnd.ms-excel',
                         add_etags=False)
    return response


def make_exc_res(exc):
    """Make flask response on call exc,`exc` is the exception object."""
    if isinstance(exc, MaitreyaExc):
        dct = dict(code=exc.exc_code, msg=exc.msg)
        return make_response(jsonpickle_dumps(dct), exc.http_code)
    elif isinstance(exc, HTTPException):
        dct = dict(code=exc.code, msg=exc.description)
        return make_response(jsonpickle_dumps(dct), exc.code)
    else:
        dct = dict(msg="Internal Error.", code=500)
        return make_response(jsonpickle_dumps(dct), getattr(exc, 'exc_code', 500))


def make_customize_res(code=200, msg='', data=''):
    """用户自定义Response."""
    dct = dict(code=code, msg=msg, data=data)
    return make_response(jsonpickle_dumps(dct))


def make_no_permission_res(msg=u'没有权限!'):
    dct = dict(code=403, msg=msg, data=None)
    return make_response(jsonpickle_dumps(dct), 200)


def make_login_required_res():
    dct = dict(code=401, msg='login required.', data=None)
    return make_response(jsonpickle_dumps(dct), 200)


def make_invalid_token_res():
    """无效的Token,用于蜂鸟团队."""
    return make_customize_res(
        code='ERR_WEBAPI_1000001',
        msg=u'Token失效,请重新登录')


def headers(header_dict):
    """This decorator adds the headers passed in to the response."""

    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, (Response, wResponse)):
                resp = result
            else:
                resp = make_response(result)

            h = resp.headers
            for header, value in header_dict.items():
                h[header] = value
            return resp

        return decorated_function

    return decorator


json_header = headers({'Content-Type': 'application/json'})
html_header = headers({'Content-Type': 'text/html'})

header_map = {
    "json": json_header,
    "html": html_header,
}
