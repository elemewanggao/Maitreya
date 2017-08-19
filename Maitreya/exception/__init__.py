#!/usr/bin/env python2
# coding=utf8
# from werkzeug.exceptions import HTTPException
from .exc_code import EXC_CODE

HTTP_OK_REQUEST = 200
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED_REQUEST = 401
HTTP_FORBIDDEN_REQUEST = 403
HTTP_SYS_ERROR = 500


class UnprocessableExc(Exception):
    """
    Exception that Used if the request is well formed, but the instructions are otherwise
    incorrect.
    """
    def __init__(self, UnprocessableEntity):
        self.data = UnprocessableEntity.data

    def get_exc_params(self):
        """get the params in UnprocessableEntity exception."""
        params = self.data.get('messages')
        return params

    def parse_exc_messages(self, messages):
        """parse exception messages."""
        message = ''
        for k, v in messages.iteritems():
            if isinstance(v, list):
                message += '%s\n' % (''.join(str(e) for e in v))
            elif isinstance(v, dict):
                message += '%s\n' % (self.parse_exc_messages(v))
        return message

    def get_exc_messages(self):
        """get exception messages to return customer."""
        return self.parse_exc_messages(self.get_exc_params())


class MaitreyaExc(Exception):
    """Maitreya自定义异常."""

    def __init__(self, exc_code, exc_type, http_code, msg):
        super(MaitreyaExc, self).__init__(msg)
        self.exc_code = exc_code
        self.exc_type = exc_type
        self.http_code = http_code
        self.msg = msg

    def __str__(self):
        return u'{}: exc[{}]:{} http[{}]'.format(
            self.exc_type, self.exc_code, self.msg, self.http_code)


class UserExc(MaitreyaExc):
    """用户异常."""

    def __init__(self, exc_code, msg, http_code=HTTP_OK_REQUEST):
        super(UserExc, self).__init__(
            exc_type='user_exc', exc_code=exc_code, http_code=http_code, msg=msg)


class AuthExc(MaitreyaExc):
    """认证异常."""

    def __init__(self, exc_code, msg, http_code=HTTP_UNAUTHORIZED_REQUEST):
        super(AuthExc, self).__init__(
            exc_type='auth_exc', exc_code=exc_code, http_code=http_code, msg=msg)


class SysExc(MaitreyaExc):
    """系统异常."""

    def __init__(self, exc_code, msg, http_code=HTTP_SYS_ERROR):
        super(SysExc, self).__init__(
            exc_type='sys_exc', exc_code=exc_code, http_code=http_code, msg=msg)


class PermissionExc(MaitreyaExc):
    """权限异常."""

    def __init__(self, exc_code, msg, http_code=HTTP_FORBIDDEN_REQUEST):
        super(SysExc, self).__init__(
            exc_type='sys_exc', exc_code=exc_code, http_code=http_code, msg=msg)


class CustomExc(MaitreyaExc):
    """自定义异常."""

    def __init__(self, exc_code, msg, http_code=HTTP_OK_REQUEST):
        super(CustomExc, self).__init__(
            exc_type='custom_exc', exc_code=exc_code,
            http_code=http_code, msg=msg)


def gen_exception_raiser(exc_cls):
    """异常生成器."""
    def wrapper(code, *args, **kwargs):
        exc_code = EXC_CODE.get(code)
        if not exc_code:
            raise SysExc(exc_code['SERVER_UNKNOWN_ERROR'][0],
                         exc_code['SERVER_UNKNOWN_ERROR'][1])
        code = exc_code[0]
        msg = exc_code[1]

        if args:
            raise exc_cls(code, msg.format(*args))
        elif kwargs:
            raise exc_cls(code, msg.format(**kwargs))
        else:
            raise exc_cls(code, msg)

    return wrapper


raise_server_exc = gen_exception_raiser(SysExc)

raise_user_exc = gen_exception_raiser(UserExc)

raise_auth_exc = gen_exception_raiser(AuthExc)

raise_permission_exc = gen_exception_raiser(PermissionExc)

raise_custom_exc = gen_exception_raiser(CustomExc)
