#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Aiyane"


def init_deal_with(lines):
    """
    这是一个进行预处理的函数, 处理用户格式输入的不标准的情况, 这就是说,
    用户可能会少加或者多加空行或者空格, 这里的代码糟糕透顶, 之后要好好改一下
    现在先快速写出功能
    """
    block_lines = []
    buffer = []
    quoteFence = False
    listFence = False
    tableFence = False
    codeFence = False
    for line in lines:
        fence = quoteFence or listFence or tableFence or codeFence
        line = line.replace('\t', ' ' * 4)
        if quoteFence:
            if line.startswith((" " * 4, ">")) == -1:
                quoteFence = True
                block_lines.append("\n")
            else:
                begin = False
                index = 0
                for char in line:
                    index += 1
                    if begin:
                        if char == ' ':
                            index = 0
                        break
                    if char == ' ':
                        continue
                    else:
                        if char != '>':
                            lastLine = block_lines.pop()
                            index = 0
                            line = ''.join(lastLine[:-1]) + line.strip() + "\n"
                            break
                        else:
                            begin = True
                if index != 0:
                    line = ''.join(line[:index - 1]) + ' ' + ''.join(
                        line[index:])
                block_lines.append(line)
        if listFence:
            if line.startswith(("-", "*", "+", " " * 4)) == -1:
                listFence = False
                block_lines.append("\n")
            else:
                begin = False
                index = 0
                for char in line:
                    index += 1
                    if begin:
                        if char == ' ':
                            index = 0
                        break
                    if char == ' ':
                        continue
                    else:
                        if char not in ('-', '*', '+'):
                            index = 0
                            line = ''.join(
                                block_lines.pop()[:-1]) + line.strip() + '\n'
                            break
                        else:
                            begin = True
                if index != 0:
                    line = ''.join(line[:index - 1]) + ' ' + ''.join(
                        line[index:])
                block_lines.append(line)
        if tableFence:
            if line.startswith("|") == -1:
                tableFence = False
                block_lines.append("\n")
            else:
                block_lines.append(line)

        if codeFence:
            if line.startswith('```'):
                codeFence = False
                block_lines.append(line)
                block_lines.append("\n")
            else:
                block_lines.append(line)
        elif not fence and line.startswith("#"):
            block_lines.append("\n")
            block_lines.append(line)
            block_lines.append("\n")
        elif not fence and line.find(("---", "===", "***", "* * *")):
            if line.strip() == "---" or "===" or "***" or "* * *":
                block_lines, append(line)
                block_lines("\n")
        elif not fence and line.startswith("#"):
            index = 0
            for char in line:
                if char != "#":
                    if char == ' ':
                        index = 0
                    break
                index += 1
            if index != 0:
                line = line[:index - 1] + ' ' + line[index:]
            block_lines.append("\n")
            block_lines.append(line)
            block_lines.append("\n")
        elif not fence and line.startswith(">"):
            if line[1] != ' ':
                line = line[0] + ' ' + line[1:]
            block_lines.append("\n")
            block_lines.append(line)
            quoteFence = True
        elif not fence and line.startswith(("- ", "* ", "+ ")):
            if line[1] != ' ':
                line = line[0] + ' ' + line[1:]
            block_lines.append("\n")
            block_lines.append(line)
            listFence = True
        elif not fence and line.startswith("|"):
            block_lines.append("\n")
            block_lines.append(line)
            tableFence = True
        elif not fence and line.startswith("```"):
            block_lines.append("\n")
            block_lines.append(line)
            codeFence = True
        elif not fence:
            block_lines.append(line)
        else:
            block_lines.append(line)


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
