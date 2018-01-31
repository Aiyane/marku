#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Aiyane'


def deal_with_line(content, token_types, init_token):
    """处理行内Token, 最开始写的代码太丑了, 最后精简到20行以内, 同时修复了之前的Bug
    参数:
        :index: 这是一个列表, 0号位表示起始位置, 1号位表示匹配的末尾位置
        :minIndex: 这是匹配的起始位置, 我们需要找出近匹配的位置
        :init_token: 这是默认的匹配Token， 用于匹配没有找到的Token类型， 一般默认为段落
        :close_token: 这是生成的Token的buffer
    """
    index = [0, 0]
    while 1:
        close_token = None
        minIndex = len(content)
        for token_type in token_types:
            match_obj = token_type.pattern.search(content, index[0])
            if match_obj and index[0] <= match_obj.start() < minIndex:
                minIndex = match_obj.start()
                close_token = token_type(match_obj)
                index[1] = match_obj.end()
        # 如果起始位置并不是第一个匹配的位置就在前段生成默认类型
        yield init_token(
            content[index[0]:minIndex]) if index[0] < minIndex else None
        if not close_token:
            break
        # 如果匹配到了就让起始位置改变， 再考察后面的字符
        index[0] = index[1]
        yield close_token
