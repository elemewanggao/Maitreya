#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webargs.flaskparser import FlaskParser
from webargs import core
import copy


class ArgsParser(FlaskParser):
    ''' Maitreya的parser'''

    __location_map__ = copy.deepcopy(FlaskParser.__location_map__)
    __location_map__.update({"url": "parse_view_args"})
    DEFAULT_LOCATIONS = ("querystring", "form", "json", "url")

    def parse_view_args(self, req, name, field):
        """Pull a url value from the request."""
        return core.get_value(req.view_args, name, field)


args_parser = ArgsParser()
