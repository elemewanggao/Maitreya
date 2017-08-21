#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
from functools import wraps
from flask import request
from .api import ApiCtx
from .log import (
    get_logger,
    log_request_info,
    log_info,
    log_warn,
    log_error)
from Maitreya.exception import (
    UserExc,
    SysExc,
    CustomExc,
)
from .response import (
    make_res,
    make_exc_res,
)

from flask import current_app

buildin_methods = ["get", "gets", "post", "put", "patch", "upload", "delete"]
log_type_signal_map = {
    'user_exc': log_warn,
    'sys_exc': log_error,
    'unexcepted_exc': log_error,
    'ok': log_info,
    'custom_exc': log_warn,
}


logger = get_logger(__name__)


def api(rule='/', **options):
    """ API decorator for Maitreya api."""
    api_ctx = ApiCtx()

    def _wrapper(func):
        if rule:
            _cache_api(func, rule, options)

        @wraps(func)
        def wrapper(*args, **kwargs):

            api_ctx.func = func
            api_ctx.req = request
            api_ctx.started_at = time.time()
            module_name = func.func_globals['__name__']
            api_ctx.module = module_name
            log_request_info(api_ctx)

            if request.method == 'OPTIONS':
                response = current_app.make_default_options_response()
                api_ctx.response = make_res(response)
                log_info(api_ctx)
            else:
                try:
                    rv = func(*args, **kwargs)
                except UserExc as exc:
                    api_ctx.exc = exc
                    api_ctx.response = make_exc_res(exc)
                    log_type = exc.exc_type
                except SysExc as exc:
                    api_ctx.exc = exc
                    api_ctx.response = make_exc_res(exc)
                    log_type = exc.exc_type
                except CustomExc as exc:
                    api_ctx.exc = exc
                    api_ctx.response = make_exc_res(exc)
                    log_type = exc.exc_type
                except Exception:
                    api_ctx.exc = sys.exc_info()[1]
                    api_ctx.response = make_exc_res(api_ctx.exc)
                    log_type = 'unexcepted_exc'
                else:
                    api_ctx.response = make_res(rv)
                    log_type = 'ok'
                finally:
                    log_type_signal_map[log_type](api_ctx)

            return api_ctx.response

        return wrapper

    return _wrapper


def _cache_api(func, rule, options):
    """生成一个func的属性，map{函数名: [(rule, {'methods':['GET', 'POST']})]}"""
    if rule is not None:
        if options.get('methods') is None:
            if func.__name__ in buildin_methods:
                options.update(methods=[func.__name__.upper()])
            else:
                options.update(methods=["GET"])
        if not hasattr(func, 'api_cache') or func.api_cache is None:
            func.api_cache = {func.__name__: [(rule, options)]}
        elif func.__name__ not in func.api_cache:
            func.api_cache[func.__name__] = [(rule, options)]
        else:
            func.api_cache[func.__name__].append((rule, options))
