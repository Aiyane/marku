#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from marku import big_token, little_token

# 注册新语法
__token__ = ['DotToken', 'NewToken']
__func__ = ['DotTokenRender', 'NewTokenRender']


# 多行语法
class DotToken(big_token.BaseBigToken):
    def __init__(self, lines):
        super().__init__(''.join(lines[1:-1]), little_token.deal_with_line)

    @staticmethod
    def match(lines):
        if len(lines) > 1 and lines[0].strip(
        ) == '...' and lines[-1].strip() == '...':
            return True
        return False


def DotTokenRender(md, token):
    return '<p>=====我的自定义语法内容=====<br/>' + md.render_line(
        token) + '</br>=======================</p>'
    # return '<p>=====我的自定义语法内容=====<br/>' + token.content +
    # '</br>=======================</p>'


# 行内语法
class NewToken(little_token.BaseLittleToken):

    pattern = re.compile(r'\!(.+?)\!')

    def __init__(self, match_obj):
        self.content = match_obj.group(1)


def NewTokenRender(md, token):
    return '<strong>' + token.content + '</strong>'


class TimeTable(big_token.BaseBigToken):
    """
    时刻表处理类
    &
    title
    kid_title|content
    kid_title|content
    &
    """

    def __init__(self, lines):
        all_contents = lines[1:-1]
        self.title = all_contents.pop(0)
        self.value = dict()
        for line in all_contents:
            key, value = line.strip().split("|")
            self.value[key] = value

    @staticmethod
    def match(lines):
        if len(lines) >= 3 and lines[0] == "&" and lines[-1] == "&":
            return True
        return False


def TimeTableRender(md, token):
    pass


class ProgressBar(big_token.BaseBigToken):
    """
    进度条处理类
    %
    title
    item|20|100
    item|60|100
    item|20|100
    %
    """

    def __init__(self, lines):
        all_content = lines[1:-1]
        self.title = all_content[0]
        content = all_content[1:]
        self.value = dict()
        for line in content:
            item, m, a = line.split('|')
            self.value[item] = [m, a]

    @staticmethod
    def match(lines):
        if len(lines) > 1 and lines[0] == "%" and lines[-1] == '%':
            return True
        return False


def ProgressBarRender(md, token):
    pass
