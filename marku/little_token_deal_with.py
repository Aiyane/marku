#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Aiyane'


def deal_with_line(content, token_types, init_token):
    """处理行内Token
    参数:
        :start:表示起始位置
        :end:表示匹配的末尾位置
        :minIndex: 这是匹配的起始位置, 我们需要找出近匹配的位置
        :init_token: 这是默认的匹配Token， 用于匹配没有找到的Token类型， 一般默认为段落
        :close_token: 这是生成的Token的buffer
    """
    start = end = 0
    while 1:
        close_token = None
        minIndex = len(content)
        for token_type in token_types:
            match_obj = token_type.pattern.search(content, start)
            if match_obj and start <= match_obj.start() < minIndex:
                minIndex = match_obj.start()
                close_token = token_type(match_obj)
                end = match_obj.end()
        # 如果起始位置并不是第一个匹配的位置就在前段生成默认类型
        yield init_token(
            content[start:minIndex]) if start < minIndex else None
        if not close_token:
            break
        # 如果匹配到了就让起始位置改变， 再考察后面的字符
        start = end 
        yield close_token
