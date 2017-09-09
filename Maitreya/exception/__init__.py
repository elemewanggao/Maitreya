#!/usr/bin/env python2
# -*- coding:utf-8 -*-
from .code import EXC_CODE


class MaitreyaCustomExc(Exception):
    """Maitreya自定义异常."""
    http_code = 100

    def __init__(self, exc_code, msg):
        super(MaitreyaCustomExc, self).__init__(msg)
        self.exc_code = exc_code
        self.msg = msg

    def __str__(self):
        return 'exception:{}, http_code:{}, code:{}, msg:{}'.format(
            self.__class__.__name__,
            self.http_code,
            self.code,
            self.msg)


class MaitreyaUserExc(MaitreyaCustomExc):
    """用户异常."""
    http_code = 200


class MaitreyaSysExc(MaitreyaCustomExc):
    """系统异常."""
    http_code = 500


def exception_raiser(exc):
    """异常生成器."""
    def wrapper(code, *args, **kwargs):
        if code in EXC_CODE:
            icode = EXC_CODE[code][0]
            msg = EXC_CODE[code][1]

            if args:
                raise exc(icode, msg.format(*args))
            elif kwargs:
                raise exc(icode, msg.format(**kwargs))
            else:
                raise exc(icode, msg)
        else:
            raise MaitreyaSysExc(500, 'unknow exception')

    return wrapper


raise_user_exc = exception_raiser(MaitreyaUserExc)

raise_sys_exc = exception_raiser(MaitreyaSysExc)
