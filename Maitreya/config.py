# -*- coding:utf-8 -*-


class HandlerConfig(object):
    """处理器配置类，对处理器配置列表解析，处理器配置如下所示.

    appeal_config = [
            {
                "handler": "get_appeal_handlers",
                "authentication": ["login"],
                "params": {
                    "carrier_type": fields.Int()},
                "return_format": "html",
                "validator":[]
            },
            ......
        ]
    """
    confs = []
    handler_obj = None

    def __init__(self, handler_name):
        self.handler_name = handler_name
        self.conf = self.get_handler_config()

    def get_confs(self):
        """获取配置列表."""
        return self.confs

    def get_handler_obj(self):
        """获取处理器对象."""
        return self.handler_obj

    def get_handler_config(self):
        """获取当前处理器配置信息."""
        for conf in self.get_confs():
            if conf['handler'] == self.handler_name:
                return conf

    def get_handler_name(self):
        """获取处理器名称."""
        if self.conf:
            return self.conf.get('handler')

    def get_handler_func(self):
        """获取处理器函数."""
        if self.get_handler_obj:
            return getattr(self.get_handler_obj(), self.get_handler_name())
        else:
            return self.get_handler_name()

    def get_handler_authentication(self):
        """获取处理器配置认证信息."""
        if self.conf:
            return self.conf.get('authentication')

    def get_handler_params(self):
        """获取处理器配置参数信息."""
        if self.conf:
            return self.conf.get('params', {})

    def get_handler_return_format(self):
        """获取处理器返回内容的格式."""
        if self.conf:
            return self.conf.get('return_format')

    def get_handler_validator(self):
        """获取处理器的校验器列表."""
        if self.conf:
            return self.conf.get('validator')


class GenServiceConfigClass(object):
    """生成服务配置类."""
    def __init__(self, confs, handler_obj=None):
        self.confs = confs
        self.handler_obj = handler_obj

    def gen_config_class(self, name):
        """生成配置类.
        params: name:配置类名称
        """
        return type(name, (HandlerConfig,), {'confs': self.confs, 'handler_obj': self.handler_obj})
