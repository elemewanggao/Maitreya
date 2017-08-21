#!/usr/bin/env python
# -*- coding: utf-8 -*-
from werkzeug.exceptions import BadRequest
import time
import logging


def get_logger(name):
    """获取日志对象."""
    return logging.getLogger(name)


def get_request_args(ctx, include=None, exclude=None):
    default_include = ('args', 'json', 'form', 'data')
    if include is None:
        include = default_include
    if exclude is not None:
        include = include - exclude

    args_dict = {}
    if 'args' in include:
        if ctx.req.args:
            args_dict['args'] = ctx.req.args.to_dict()
    if 'json' in include:
        try:
            if ctx.req.json:
                args_dict['json'] = ctx.req.json
        except BadRequest:
            pass
    if 'form' in include:
        if ctx.req.form:
            args_dict['form'] = ctx.req.form
    if 'data' in include:
        if ctx.req.data:
            args_dict['data'] = ctx.req.data
    if 'headers' in include:
        if ctx.req.headers:
            args_dict['headers'] = ctx.req.headers
    if 'cookies' in include:
        if ctx.req.cookies:
            args_dict['cookies'] = ctx.req.cookies
    return args_dict


def log_info(ctx):
    log = logging.getLogger(name=ctx.module)
    timed = (time.time() - ctx.started_at) * 1000  # ms
    url = ctx.req.url[len(ctx.req.url_root) - 1:]

    req_data = get_request_args(ctx)

    fmt = ('{ctx.req.method} {url} {req_data}'
           ' => {ctx.module}.{call} => {ctx.response.status_code}'
           ' => {timed:.3f}ms')

    return log.info(fmt.format(ctx=ctx, call=ctx.func.__name__, url=url,
                               timed=timed, req_data=req_data))


def log_request_info(ctx):
    log = logging.getLogger(name=ctx.module)
    url = ctx.req.url[len(ctx.req.url_root) - 1:]

    req_data = get_request_args(ctx)

    fmt = ('{ctx.req.method} {url} {req_data}'
           ' => {ctx.module}.{call}')
    return log.info(fmt.format(ctx=ctx, call=ctx.func.__name__, url=url,
                               req_data=req_data))


def log_warn(ctx):
    log = logging.getLogger(name=ctx.module)
    url = ctx.req.url[len(ctx.req.url_root) - 1:]
    req_data = get_request_args(ctx)

    fmt = ('{ctx.req.method} {url} {req_data}'
           ' => {ctx.module}.{call} => {ctx.response.status_code}')
    return log.warn(fmt.format(ctx=ctx, call=ctx.func.__name__, url=url,
                               req_data=req_data), exc_info=True)


def log_error(ctx):
    log = logging.getLogger(name=ctx.module)
    url = ctx.req.url[len(ctx.req.url_root) - 1:]
    req_data = get_request_args(ctx)

    fmt = ('{ctx.req.method} {url} {req_data}'
           ' => {ctx.module}.{call} => {ctx.response.status_code}')
    return log.error(fmt.format(ctx=ctx, call=ctx.func.__name__, url=url,
                                req_data=req_data), exc_info=True)
