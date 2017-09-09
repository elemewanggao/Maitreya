# -*- coding:utf-8 -*-
"""URL管理器."""
import requests
from bs4 import BeautifulSoup
from Maitreya.models.url import TbUrl


class Url(object):
    """url"""
    request_method_handler_map = {
        'GET': requests.get,
        'POST': requests.post,
        'PUT': requests.put,
        'DELETE': requests.delete,
        'HEAD': requests.head,
        'OPTIONS': requests.options
    }

    def __init__(self, url, method='GET', params={}, header={}, data={}, json={}, cookie='', user='', passport=''):
        """初始化URL"""
        self.url = url
        self.method = method
        self.params = params
        self.header = header
        self.data = data
        self.json = json
        self.cookie = cookie
        self.user = user
        self.passport = passport
        self.request_handler = self.request_method_handler_map.get(self.method)

    def set_crawl_method(self):
        """设置URL爬取方式."""
        pass

    def get_crawl_method(self):
        """获取URL爬取方式."""
        pass

    def download(self):
        """根据URL信息进行下载,返回下载网页内容."""
        response = self.request_handler(self.url, params=self.params, headers=self.header, data=self.data, json=self.json)
        return response.text

    def parse(self, text):
        """根据下载器下载的内容和URL爬取方式进行解析,解析结果为:标题，内容（包括图片），日期，出处, 标签"""
        content = BeautifulSoup(text, "lxml")

        """to do"""


class UrlManager(object):
    url_list = []

    def get_crawled_urls(self):
        """获取爬过的URL列表(成员)."""
        return TbUrl.query(
            [TbUrl.method, TbUrl.url],
            filter=[TbUrl.is_crawled == 1])

    def get_uncrawled_urls(self):
        """获取未爬过的URL(成员)."""
        return TbUrl.query(
            [TbUrl.method, TbUrl.url],
            filter=[TbUrl.is_crawled == 0])

    def set_url_crawled(self, url):
        """将url爬取状态置为已爬取."""
        TbUrl.update({'is_crawled': 1}, [TbUrl.id == url.id])

    def add_url_to_url_list(self, url):
        """将URL加入待爬取列."""
        if not self.is_in_url_list(url):
            self.url_list.append(url)

    def is_in_url_list(self, url):
        """判断url是否已经放进URL容器内."""
        for u in self.url_list:
            if u.url == url.url and u.method == url.method:
                return True
        return False

