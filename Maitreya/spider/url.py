# -*- coding:utf-8 -*-
"""URL管理器."""


class Url(object):
    """url"""
    def __init__(self, url, method='GET', cookie='', user='', passport=''):
        """初始化URL"""
        pass

    def set_crawl_method(self):
        """设置URL爬取方式."""
        pass

    def get_crawl_method(self):
        """获取URL爬取方式."""
        pass

    def download(self):
        """根据URL信息进行下载,返回下载网页内容."""
        pass

    def parse(self):
        """根据下载器下载的内容和URL爬取方式进行解析,解析结果为:标题，内容（包括图片），日期，出处, 标签"""
        pass


class UrlManager(object):
    def get_crawled_urls(self):
        """获取爬过的URL列表(成员)."""
        pass

    def get_uncrawled_urls(self):
        """获取未爬过的URL(成员)."""
        pass

    def add_url_to_crawled_list(self, url):
        """将url加入已经爬取列表.如果url在待爬取列表中，要先删除."""
        pass

    def add_url_to_uncrawled_list(self, url):
        """将URL加入待爬取列表中."""
        pass

