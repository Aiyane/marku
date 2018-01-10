#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Aiyane"


def deal_with(lines, token_types, init_token, root=None):
    """这是一个Token处理函数, 需要注意的是代码块中需要保留空行,所以单独对代码块进行了处理

    :lines: 多行列表
    :token_types: 处理的Token类型
    :deal_func: 默认Token
    :root: 根结点
    :returns: 返回Token

    """
    is_code = False
    line_buffer = []
    for line in lines:
        line = line.replace('\t', ' ' * 4)
        if is_code or line != '\n':
            line_buffer.append(line)
            if line.startswith('```'):
                is_code = not is_code
        elif line == '\n' and line_buffer:
            yield find_token(line_buffer, token_types, init_token)
            line_buffer.clear()


def find_token(line_buffer, token_types, init_token):
    """
    这是一个构造块级Token的函数, 没有匹配到, 用默认Token构造
    """
    for token_type in token_types:
        if token_type.match(line_buffer):
            return token_type(line_buffer)
    return init_token(line_buffer)
