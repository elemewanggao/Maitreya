#!/usr/bin/env python
# -*- coding: utf-8 -*-

from werkzeug.exceptions import BadRequest
import threading


class Ctx(threading.local):
    def update(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    def clear(self):
        return self.__dict__.clear()


class ApiCtx(Ctx):
    def __init__(self, module=None, func=None, req=None, started_at=None,
                 exc=None, response=None, user=None, logger=None):
        self.req = req
        self.exc = exc
        self.func = func
        self.module = module
        self.response = response
        self.started_at = started_at
        self.user = user
        self.logger = logger

    def get_request_args(self, include=None, exclude=None):
        """获取请求参数."""
        default_include = ('args', 'json', 'form', 'data')
        if include is None:
            include = default_include
        if exclude is not None:
            include = include - exclude

        args_dict = {}
        if 'args' in include:
            if self.req.args:
                args_dict['args'] = self.req.args.to_dict()
        if 'json' in include:
            try:
                if self.req.json:
                    args_dict['json'] = self.req.json
            except BadRequest:
                pass
        if 'form' in include:
            if self.req.form:
                args_dict['form'] = self.req.form
        if 'data' in include:
            if self.req.data:
                args_dict['data'] = self.req.data
        if 'headers' in include:
            if self.req.headers:
                args_dict['headers'] = self.req.headers
        if 'cookies' in include:
            if self.req.cookies:
                args_dict['cookies'] = self.req.cookies
        return args_dict
