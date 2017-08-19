#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging


class Logger(object):

    def get_logger(self, name):
        """获取日志对象."""
        return logging.getLogger(name)


class LogApi(Logger):
    """记录API日志."""

    def log_init(self, api):
        self.logger = self.get_logger(api.module)
        self.url = api.req.url[len(api.req.url_root) - 1:]
        self.req_data = api.get_request_args()
        self.time = (time.time() - api.started_at) * 1000  # ms

    def log_api_info(self, api):
        self.log_init(api)
        """正常API日志,包含请求和响应."""
        fmt = ('user:{api.user} {api.req.method} {url} {req_data}'
               ' => {api.module}.{call} => {api.response.status_code}'
               ' => {timed:.3f}ms')

        return self.logger.info(fmt.format(api=api, call=api.func.__name__, url=self.url,
                                           timed=self.time, req_data=self.req_data))

    def log_request_info(self, api):
        self.log_init(api)
        """正常请求日志."""
        fmt = ('user:{api.user} {api.req.method} {url} {req_data}'
               ' => {api.module}.{call}')
        return self.logger.info(fmt.format(api=api, call=api.func.__name__, url=self.url,
                                           req_data=self.req_data))

    def log_warn(self, api):
        """警告日志"""
        self.log_init(api)
        fmt = ('user:{api.user} {api.req.method} {url} {req_data}'
               ' => {api.module}.{call} => {api.response.status_code}')
        return self.logger.warn(fmt.format(api=api, call=api.func.__name__, url=self.url,
                                           req_data=self.req_data), exc_info=True)

    def log_error(self, api):
        self.log_init(api)
        """错误日志."""
        fmt = ('user:{api.user} {api.req.method} {url} {req_data}'
               ' => {api.module}.{call} => {api.response.status_code}')
        return self.logger.error(fmt.format(api=api, call=api.func.__name__, url=self.url,
                                            req_data=self.req_data), exc_info=True)


get_logger = Logger().get_logger
log = LogApi()
