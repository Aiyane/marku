#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 处理行内的小Token
__author__ = 'Aiyane'
import re
import marku.little_token_deal_with as deal_wither
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
    return deal_wither.deal_with_line(content, _token_types, RawText)


class BaseLittleToken(object):
    """行内基础Token"""

    def __init__(self, match_obj):
        """构造函数

        :match_obj: 通过正则表达式, 匹配到的

        """
        self._kids = tuple( token for token in deal_with_line(match_obj.group(1)))

    # 用这个装饰器将方法变成一个属性, 只在调用的时候构造
    @property
    def kids(self):
        if isinstance(self._kids, GeneratorType):
            self._kids = tuple(self._kids)
        return self._kids


class RawText(BaseLittleToken):
    """这是一个纯文本的Token"""

    def __init__(self, raw):
        """构造函数
        """
        self.content = raw


class EscapeCharToken(BaseLittleToken):
    """逃逸字符Token, 例如(\#)"""

    pattern = re.compile(r"\\([\*\(\)\[\]\~])")

    def __init__(self, match_obj):
        """构造函数
        """
        self._kids = (RawText(match_obj.group(1)), )


class EmphasisToken(BaseLittleToken):
    """这是一个斜体的Token
    例如('*斜体*', '_斜体_')
    """
    pattern = re.compile(r"\*((?:\*\*|[^\*])+?)\*(?!\*)|_((?:__|[^_])+?)_")

    def __init__(self, match_obj):
        """构造函数
        """
        self._kids = (
            RawText(
                next(group for group in match_obj.groups()
                     if group is not None)), )


class StrongToken(BaseLittleToken):
    """这是一个强调的Token
    例如('**强调**', '__强调__')
    """
    pattern = re.compile(r"\*\*(.+?)\*\*(?!\*)|__(.+)__(?!_)")

    def __init__(self, match_obj):
        """构造函数
        """
        self._kids = (
            RawText(
                next(group for group in match_obj.groups()
                     if group is not None)), )


class InlineCodeToken(BaseLittleToken):
    """这是一个行内代码的Token
    例如('`code`')
    """
    pattern = re.compile(r"`(.+?)`")

    def __init__(self, match_obj):
        """构造函数
        """
        self._kids = (RawText(match_obj.group(1)), )


class DeleToken(BaseLittleToken):
    """这是一个删除符Token
    例如('~~删除符~~')
    """
    pattern = re.compile(r"~~(.+?)~~")

    def __init__(self, match_obj):
        """构造函数
        """
        self._kids = tuple(RawText(match_obj.group(1)), )


class ImageToken(BaseLittleToken):
    """这是图片的Token
    例如( '![alt](src "title")' )
    """
    pattern = re.compile(r'\!\[(.+?)\] *\((.+?)(?: *"(.+?)")?\)')

    def __init__(self, match_obj):
        self._kids = (RawText(match_obj.group(1)), )
        self.src = match_obj.group(2)
        self.title = match_obj.group(3)


class LinkToken(BaseLittleToken):
    """这是一个链接的Token
    例如('[name](target)')
    """
    pattern = re.compile(
        r"\[((?:!\[(?:.+?)\][\[\(](?:.+?)[\)\]])|(?:.+?))\] *\((.+?)\)")

    def __init__(self, match_obj):
        """构造函数
        """
        self._kids = (RawText(match_obj.group(1)), )
        self.target = match_obj.group(2)


class AutoLinkToken(BaseLittleToken):
    """这是一个自动链接的Token
    例如('<https://www.baidu.com>')
    """
    pattern = re.compile(r"<([^ ]+?)>")

    def __init__(self, match_obj):
        """构造函数
        """
        self._kids = (RawText(match_obj.group(1)), )
        self.target = match_obj.group(1)


# 这是能够构造的行内Token
_token_types = [
    InlineCodeToken, EscapeCharToken, EmphasisToken, StrongToken,
    DeleToken, ImageToken, LinkToken, AutoLinkToken
]
