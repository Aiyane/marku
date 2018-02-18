#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from marku import big_token, little_token

__token__ = ['DotToken', 'NewToken']
__func__ = ['DotTokenRender', 'NewTokenRender']


class DotToken(big_token.BaseBigToken):
    def __init__(self, lines):
        self.content = ''.join(lines[1:-1])

    @staticmethod
    def match(lines):
        if len(lines) > 1 and lines[0].strip() == '...' and lines[-1].strip() == '...':
            return True
        return False


def DotTokenRender(token):
    return '<p>=====我的自定义语法内容=====<br/>' + token.content + '</br>========就在上面=======</p>'


class NewToken(little_token.BaseLittleToken):

    pattern = re.compile(r'\!(.+?)\!')

    def __init__(self, match_obj):
        self.content = match_obj.group(1)


def NewTokenRender(token):
    return '<strong>' + token.content + '</strong>'
