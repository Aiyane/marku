#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Aiyane'
import re
from marku import big_token
from marku import little_token

__token__ = ['HTMLBigToken', 'HTMLLittleToken']


class HTMLBigToken(big_token.BaseBigToken):
    """这是一个处理块级HTML标签的Token"""

    def __init__(self, lines):
        """构造函数
        """
        self.content = ''.join(lines).replace('\n', '')

    @staticmethod
    def match(lines):
        open_tag_end = lines[0].find('>')
        close_tag_start = lines[-1].find('</')
        if (not lines[0].strip().startswith('<') or open_tag_end == -1
                or close_tag_start == -1):
            return False
        open_tag = lines[0][1:open_tag_end].split(' ')[0]
        close_tag = lines[-1][close_tag_start + 2:-2]
        if open_tag != close_tag:
            return False
        return True


class HTMLLittleToken(little_token.BaseLittleToken):
    """这是一个处理行内HTML的Token"""

    pattern = re.compile(r"<([A-z0-9]+?)(?: .+?)?(?: ?/>|>.*?<\/\1>)")

    def __init__(self, match_obj):
        """构造函数
        """
        self.content = match_obj.group(0)
