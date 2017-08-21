#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
