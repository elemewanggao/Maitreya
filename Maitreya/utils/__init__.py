#!/usr/bin/env python
# -*- coding: utf-8 -*-
import jsonpickle


def jsonpickle_dumps(obj, **kwargs):
    kwargs.setdefault('unpicklable', False)
    return jsonpickle.encode(obj, **kwargs)
