# -*- coding:utf-8 -*-
import re


def get_match_str_by_regular(content, regex):
    """获取正则匹配对象."""
    p = re.compile(r'{}'.format(regex))
    return p.search(str(content))


def regular_express_match(content, regex, index=1):
    """正则表达式匹配.
        :params:
        content:待匹配的字符串
        regex:正则表达式
        index:获取匹配的内容的索引,默认返回第一个匹配的内容
    """
    m = get_match_str_by_regular(content, regex)
    if m:
        return m.group(index)


def parse_paging(page_size, page_no):
    """将前端传的page_size,page_no转换成offset,limit."""
    limit = page_size
    offset = (page_no - 1) * page_size
    return limit, offset


MAX_I32 = 2147483647
MAX_I64 = 9223372036854775807
