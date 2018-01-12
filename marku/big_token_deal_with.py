#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Aiyane"


def init_deal_with(lines, tokens):
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
                quoteFence = False
                yield tokens["QuoteToken"](block_lines)
                block_lines.clear()
            else:
                block_lines.append(insert_blank(line, ('>'), block_lines))
        if listFence:
            if line.startswith(("-", "*", "+", " " * 4)) == -1:
                listFence = False
                yield tokens["ListToken"](block_lines)
                block_lines.clear()
            else:
                block_lines.append(
                    insert_blank(line, ('-', '*', '+'), block_lines))
        if tableFence:
            if line.startswith("|") == -1:
                tableFence = False
                yield tokens["TableToken"](block_lines)
                block_lines.clear()
            else:
                block_lines.append(line)

        if codeFence:
            if line.startswith('```'):
                codeFence = False
                block_lines.append(line)
                yield tokens["BlockCodeToken"](block_lines)
                block_lines.clear()
            else:
                block_lines.append(line)
        elif not fence and line.find(("---", "===", "***", "* * *")):
            if line.strip() == "---" or "===" or "***" or "* * *":
                if block_lines:
                    block_lines.append(line)
                    yield tokens["HeadToken"](block_lines)
                    block_lines.clear()
                else:
                    yield tokens["SeparatorToken"](line)
        elif not fence and line.startswith("#"):
            if block_lines:
                yield tokens["ParagraphToken"](block_lines)
                block_lines.clear()
            index = 0
            for char in line:
                if char != "#":
                    if char == ' ':
                        index = 0
                    break
                index += 1
            if index != 0:
                line = line[:index - 1] + ' ' + line[index:]
            yield tokens["HeadToken"](line)
        elif not fence and line.startswith(">"):
            if block_lines:
                yield tokens["ParagraphToken"](block_lines)
                block_lines.clear()
            if line[1] != ' ':
                line = line[0] + ' ' + line[1:]
            block_lines.append("\n")
            block_lines.append(line)
            quoteFence = True
        elif not fence and line.startswith(("- ", "* ", "+ ")):
            if block_lines:
                yield tokens["ParagraphToken"](block_lines)
                block_lines.clear()
            if line[1] != ' ':
                line = line[0] + ' ' + line[1:]
            block_lines.append("\n")
            block_lines.append(line)
            listFence = True
        elif not fence and line.startswith("|"):
            if block_lines:
                yield tokens["ParagraphToken"](block_lines)
                block_lines.clear()
            block_lines.append("\n")
            block_lines.append(line)
            tableFence = True
        elif not fence and line.startswith("```"):
            if block_lines:
                yield tokens["ParagraphToken"](block_lines)
                block_lines.clear()
            block_lines.append("\n")
            block_lines.append(line)
            codeFence = True
        else:
            block_lines.append(line)

    def insert_blank(content, value):
        """
        判断list行和quote行符号后是否有正确的空格与内容隔开, 没有就加上
        """
        begin = False
        char_index = 0
        for line_char in content:
            char_index += 1
            if begin:
                if line_char == ' ':
                    char_index = 0
                break
            if line_char == ' ':
                continue
            else:
                if line_char not in value:
                    char_ndex = 0
                    content = block_lines.pop(-1) + line.strip() + "\n"
                    break
                else:
                    begin = True
        if char_index != 0:
            content = ''.join(content[:char_index - 1]) + ' ' + ''.join(
                content[char_index:])
        return content


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
