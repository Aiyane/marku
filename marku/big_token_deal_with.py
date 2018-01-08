#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Aiyane"

class continueLine(str):

    """这是一个持续的行, 虽然只有换行符, 但是还是要保留它, 因为它在code里"""
    def __new__(cls):
        return super().__new__(cls, '\n')

    def __eq__(self, other):
        if other == '\n':
            return False

    def __ne__(self, other):
        if other == '\n':
            return True

def init_deal(lines):
    """这是一个初始化处理lines的方法
    在```something```里面可以有空行, 所以要区分出来
    :lines: 多行
    :returns: 特殊的一行

    """
    code_fence = False
    for line in lines:
        # 格式化tabs
        line = line.replace('\t', '    ')
        if not code_fence and line.startswith('```'):
            code_fence = True
            yield '\n'
            yield line
        elif code_fence:
            if line == '```\n':
                code_fence = False
                yield line
                yield '\n'
            elif line == '\n':
                yield continueLine()
            else:
                yield line
        else:
            yield line
    if code_fence:
        code_fence = False
        yield '```\n'
        yield '\n'


def deal_with(lines, token_types, init_token, root=None):
    """这是一个Token处理函数

    :lines: 多行列表
    :token_types: 处理的Token类型
    :deal_func: 默认Token
    :root: 根结点
    :returns: 返回Token

    """
    line_buffer = []
    for line in init_deal(lines):
        # 这一段就是要区分块级的Token
        if line != '\n':
            line_buffer.append(line)
        elif line_buffer:
            token = _match_for_toBken(line_buffer, token_types, init_token, root)
            if token is not None:
                yield token
            line_buffer.clear()

def _match_for_token(line_buffer, token_types, init_token, root):
    """这是一个尝试用token_types中的类型构造Token的方法

    :line_buffer: 多行, 块级的, 是由'\n'区分出来的
    :token_types: 所有可以处理的Token类型
    :init_token: 默认处理成的Token, 一般默认为段落
    :root: 根结点, 文档Token
    :returns: 返回Token

    """
    for token_type in token_types:
        if token_type.match(line_buffer):
            return token_type(line_buffer)
    # 如果没有找到, 就返回默认类型
    return init_token(line_buffer)

