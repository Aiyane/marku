#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 处理行内的小Token
__author__ = 'Aiyane'
import re
import little_token_deal_with as deal_wither
from types import GeneratorType

__all__ = [
    'EscapeCharToken', 'EmphasisToken', 'StrongToken', 'InlineCodeToken',
    'DeleToken', 'ImageToken', 'LinkToken', 'AutoLinkToken'
]

# 以上依次为逃逸字符, 斜体, 粗体, 行内代码, 删除符, 图片, 链接, 自动链接<http://www.baidu.com>这种


def deal_with_line(content):
    """这个是处理行内Token的函数

    :content: 这是传过来的内容
    :returns: 需要被构造的Token
    :_token_types: 是全部行内Token, 见文件下面
    :RawText: 是默认构造的Token, 默认为一行纯文本
    """
    return deal_wither.deal_with(content, _token_types, RawText)


class BaseLittleToken(object):
    """行内基础Token"""

    def __init__(self, match_obj):
        """构造函数

        :match_obj: 通过正则表达式, 匹配到的

        """
        self._kids = deal_with_line(match_obj.group(1))

    # 用这个装饰器将方法变成一个属性, 只在调用的时候构造
    @property
    def kids(self):
        if isinstance(self._kids, GeneratorType):
            self._kids = tuple(self._kids)
        return self._kids


class EscapeCharToken(BaseLittleToken):
    """逃逸字符Token, 例如(\#)"""

    def __init__(self, match_obj):
        """构造函数
        """
        self._match_obj = match_obj
        pass


# 这是能够构造的行内Token
_token_types = [
    'EscapeCharToken', 'EmphasisToken', 'StrongToken', 'InlineCodeToken',
    'DeleToken', 'ImageToken', 'LinkToken', 'AutoLinkToken'
]
