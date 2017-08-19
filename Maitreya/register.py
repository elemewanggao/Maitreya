#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
from functools import wraps
from flask import request
from .api import ApiCtx
from .log import get_logger
from Maitreya.exception import (
    UserExc,
    SysExc,
    CustomExc,
)
from .response import (
    make_res,
    make_exc_res,
)
from .signal import (
    sig_call_ok,
    sig_call_done,
    sig_call_user_exc,
    sig_call_sys_exc,
    sig_call_unexcepted_exc,
    sig_call_req,
    sig_call_final,
    sig_call_custom_exc,
)

from flask import current_app, g

buildin_methods = ["get", "gets", "post", "put", "patch", "upload", "delete"]
log_type_signal_map = {
    'user_exc': sig_call_user_exc,
    'sys_exc': sig_call_sys_exc,
    'unexcepted_exc': sig_call_unexcepted_exc,
    'ok': sig_call_ok,
    'custom_exc': sig_call_custom_exc,
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
            sig_call_req.send(api_ctx)

            if request.method == 'OPTIONS':
                response = current_app.make_default_options_response()
                api_ctx.response = make_res(response)
                sig_call_ok.send(api_ctx)
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
                    api_ctx.user = g.user.email.split('@')[0] if hasattr(g, 'user') else None
                    api_ctx.logger = g.logger if hasattr(g, 'logger') else None
                    log_type_signal_map[log_type].send(api_ctx)
                    sig_call_final.send(api_ctx)

            sig_call_done.send(api_ctx)

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
