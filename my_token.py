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
        if len(lines) > 1 and lines[0].strip() == '...' and lines[-1].strip() == '...':
            return True
        return False


def DotTokenRender(md, token):
    return '<p>=====我的自定义语法内容=====<br/>' + md.render_line(token) + '</br>=======================</p>'
    # return '<p>=====我的自定义语法内容=====<br/>' + token.content + '</br>=======================</p>'


# 行内语法
class NewToken(little_token.BaseLittleToken):

    pattern = re.compile(r'\!(.+?)\!')

    def __init__(self, match_obj):
        self.content = match_obj.group(1)


def NewTokenRender(md, token):
    return '<strong>' + token.content + '</strong>'
