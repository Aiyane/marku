#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Aiyane'


def deal_with_line(content, token_types, init_token):
    """处理行内Token
    参数:
    :content: 匹配内容
    :token_types: 可以匹配的Token
    :init_token: 默认的Token

    容我解释一下这一段代码, 处理行内的文字
    index是处理的开始位置, 如果匹配到一个Token,那么

    问: 匹配的这一个Token的起始位置等于index吗?
        不是, 那么需要从index到匹配的起始位置之间包裹成默认Token
            让这是index等于匹配的起始位置, 再用匹配的Token包裹它
        是的, 那么直接包裹成匹配的Token, index指向匹配的结束位置

    每一项Token都匹配完了, 这时
    问: index等于content总长度吗?
        是的, 最后一个匹配已经将content全部匹配完
        不是, 还留有没有匹配的内容, 所以再用默认Token包裹最后的内容
    """
    index = 0

    while index < len(content):
        if_jump = index
        for token_type in token_types:
            match_obj = token_type.pattern.search(content, index)
            if match_obj and index < match_obj.start():
                index = match_obj.start()
                yield init_token(content[index:match_obj.start()])
            if match_obj.start(
            ) == index and match_obj and match_obj.start() < len(content):
                index = match_obj.end()
                yield token_type(match_obj)
                break
        if if_jump == index:
            yield init_token(content[index:])
            index = len(content)
