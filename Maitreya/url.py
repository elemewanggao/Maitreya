# -*- coding:utf-8 -*-
import functools
from werkzeug.exceptions import UnprocessableEntity
from Maitreya.exception import UnprocessableExc, raise_user_exc
from .parser import args_parser
from .register import api
import fields
from Maitreya.utils.common import regular_express_match, parse_paging
from .log import get_logger
from .config import HandlerConfig
from .response import header_map
logger = get_logger(__name__)


class Url(object):
    def __init__(self, suffix_url, service_conf_obj,
                 methods=['GET'], prefix_route='/webapi'):

        self.url = prefix_route + suffix_url.split('?')[0]
        self.methods = methods
        self.service = service_conf_obj
        self.authentication = None
        self.params = self.get_params_from_url(suffix_url)
        self.return_format, self.validators = None, None

        if isinstance(service_conf_obj, HandlerConfig):
            self.service_conf_obj = service_conf_obj
            self.service = self.service_conf_obj.get_handler_func()
            self.authentication = self.service_conf_obj.get_handler_authentication()
            self.params = self.service_conf_obj.get_handler_params()
            self.return_format = self.service_conf_obj.get_handler_return_format()
            self.validators = self.service_conf_obj.get_handler_validator()

    @staticmethod
    def page_param_to_offset_limit(params):
        """对url传入的page_no, page_size进行特殊处理，转换成接口中的需要的offset, limit."""
        if params:
            page_no = params.pop('page_no', None)
            page_size = params.pop('page_size', None)
            if page_no and page_size:
                limit, offset = parse_paging(page_size, page_no)
                params.update({'offset': offset, 'limit': limit})
        return params

    def get_params_from_url(self, suffix_url):
        """从url中获取参数."""
        if suffix_url.count('?') == 1:
            query_strs = suffix_url.split('?')[1]
            param_list = query_strs.split('&')

            regex = r'<(\w+):(\w+)=?(\w+)?>'
            params = {}
            for param in param_list:
                param_type = regular_express_match(param, regex, 1)
                param_name = regular_express_match(param, regex, 2)
                default_value = regular_express_match(param, regex, 3)

                if param_type == 'int':
                    params[param_name] = \
                        fields.Int(missing=default_value) if default_value else fields.Int()
                elif param_type == 'string':
                    params[param_name] = \
                        fields.Str(missing=default_value) if default_value else fields.Str()
            return params

    def check_handler_params(self, func):
        """校验处理器参数."""
        @functools.wraps(func)
        def inner(*args, **kwargs):
            if not self.params:
                return func(*args, **kwargs)
            try:
                params = args_parser.parse(self.params)
            except UnprocessableEntity as e:
                unpro_exc = UnprocessableExc(e)
                messages = unpro_exc.get_exc_messages()
                raise_user_exc('CUSTOM_BAD_REQUEST', message=messages)

            params = Url.page_param_to_offset_limit(params)

            kwargs.update(params)

            # 对传入的参数使用校验器校验
            if self.validators:
                for validator in self.validators:
                    validator(func)(*args, **kwargs)
            return func(*args, **kwargs)
        return inner

    def add_response_header(self):
        """增加response的头部."""
        return_format = 'json' if not self.return_format else self.return_format
        return header_map.get(return_format)

    def get_service_after_config(self):
        """通过服务配置更新服务函数."""
        result_service = self.check_handler_params(self.service)
        return result_service

    def add_url_to_route(self, app):
        """将URL绑定到路由函数上."""
        endpoint = self.url + self.service.__name__
        conf_service = self.get_service_after_config()
        header = self.add_response_header()
        logger.info('{url} {methods} {service}'.format(
            url=self.url,
            methods=self.methods,
            service=self.service.func_globals['__name__'] + '.' + self.service.__name__))
        app.add_url_rule(self.url, endpoint, header(api(None)(conf_service)), methods=self.methods)
