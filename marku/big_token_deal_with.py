#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Aiyane"


class codeLine(str):
    """这是一个持续的行, 虽然只有换行符, 但是还是要保留它, 因为它在code里"""

    def __new__(cls, line):
        return super().__new__(cls, line)

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

        if line.startswith('```'):
            if code_fence:
                yield line
                yield '\n'
                code_fence = False
            else:
                code_fence = True
                yield '\n'
                yield line
        elif code_fence:
            yield codeLine(line)
        else:
            yield line


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
            for token_type in token_types:
                if token_type.match(line_buffer):
                    yield token_type(line_buffer)
                    line_buffer.clear()
            if line_buffer:
                yield init_token(line_buffer)
                line_buffer.clear()

