#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Aiyane'
import re
import big_token
import little_token

__all__ = ['HTMLBigToken', 'HTMLLittleToken']


class HTMLBigToken(big_token.BaseBigToken):
    """这是一个处理块级HTML标签的Token"""

    def __init__(self, lines):
        """构造函数
        """
        pass


class HTMLLittleToken(little_token.BaseLittleToken):
    """这是一个处理行内HTML的Token"""

    def __init__(self, match_obj):
        """构造函数
        """
        pass
