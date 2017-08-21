# -*- coding:utf-8 -*-
from .url import Url


def hello(hello='hello'):
    return hello


common_conf = [
    Url('/hello', lambda: {'result': 'ni hao!'}),
    Url('/<string:hello>', hello)]


# 新增路由需要在此注册
route_confs = [common_conf]


def route_init(app):
    """对路由初始化."""
    url_confs = []
    for conf in route_confs:
        url_confs.extend(conf)
    for url_conf in url_confs:
        url_conf.add_url_to_route(app)
