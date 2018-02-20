#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Aiyane"


def init_deal_with(lines, tokens, init_token, root=None, extra_tokens=None):
    """
    这是一个进行预处理的函数, 处理用户格式输入的不标准的情况
    用户可能会少加或者多加空行或者空格
    参数：
        :block_lines: 代码块
        :Quote_Fence: 引用代码的栅格
        :List_Fence: 列表代码的栅格
        :Table_Fence: 表格的栅格
        :Code_Fence: 代码块的栅格
        :Blank_Fence: 四个空格开头的代码删格
    """
    block_lines = []
    Quote_Fence = False
    List_Fence = False
    Table_Fence = False
    Code_Fence = False
    Blank_Fence = False

    for line in _yield_line(lines):
        line = line.replace('\t', ' ' * 4)

        if List_Fence:
            # 列表
            if line.startswith(("*", "-", "+", " "*4)) or line.split('.')[0].isdigit():
                line = line_deal(line)
                block_lines.append(line)
                continue
            else:
                yield tokens['ListToken'](block_lines)
                block_lines.clear()
                List_Fence = False

        elif Quote_Fence:
            # 引用
            if line.strip().startswith('>'):
                line = line_deal(line)
                block_lines.append(line)
                continue
            else:
                yield tokens['QuoteToken'](block_lines)
                block_lines.clear()
                Quote_Fence = False
            
        elif Table_Fence:
            # 处理表格块
            # 这里的代码处理没有空行的能再识别接下来的语句块
            if line.startswith("|"):
                block_lines.append(line)
                continue
            else:
                Table_Fence = False
                yield tokens["TableToken"](block_lines)
                block_lines.clear()

        elif Code_Fence:
            # ```开头的代码块
            if line.startswith('```'):
                Code_Fence = False
                block_lines.append(line)
                yield tokens["BlockCodeToken"](block_lines)
                block_lines.clear()
            else:
                block_lines.append(line)
            continue

        elif Blank_Fence:
            # 空格开头的代码块
            if line.startswith(' ' * 4):
                block_lines.append(line)
                continue
            else:
                yield tokens['BlockCodeToken'](block_lines)
                block_lines.clear()
                Blank_Fence = False

        # 这里开始是每一行的判断
        # 也会接着上面语句块结束后接着判断接下来的一行
        # 也就是说, 用户即使没有按照语法标准
        # 没有一个空行, 也是会对这行语句进行判断的
        # 这样就能继续处理并不符合标准语法的语句
        token = deal_extra_token(block_lines, extra_tokens)
        if not is_mark(line) and not token:
            block_lines.append(line)
            continue
        elif token:
            yield token
            block_lines.clear()
            if not is_mark(line):
                block_lines.append(line)
                continue
        else:
            yield init_token(block_lines)
            block_lines.clear()

        if line.startswith("#"):
            # 处理标题
            line = line_deal(line)
            yield tokens["HeadToken"]([line])

        elif line.strip() in ("---", "===", "***", "* * *"):
            # 说明是分隔符
            yield tokens["SeparatorToken"]([line.strip()])

        elif line.startswith(("-", "*", "+", ">")):
            # 列表或者引用
            line = line_deal(line)
            block_lines.append(line)
            if line.startswith(">"):
                Quote_Fence = True
            else:
                List_Fence = True

        elif line.split('.')[0].isdigit():
            # 列表
            line = line_deal(line)
            block_lines.append(line)
            List_Fence = True

        elif not line.strip():
            # 空行
            continue

        else:
            block_lines.append(line)
            if line.startswith("|"):
                Table_Fence = True
            elif line.startswith(' ' * 4):
                Blank_Fence = True
            else:
                Code_Fence = True


def line_deal(line):
    # 处理用户输入不标准
    # 标题行
    if line[0] == "#":
        index = 0
        for char in line:
            if char != "#":
                if char == ' ':
                    index = 0
                break
            index += 1
        if index != 0:
            line = ''.join(line[:index]) + ' ' + ''.join(line[index:])

    # 引用行
    elif line.strip().startswith('>'):
        line = '> ' + line.strip()[1:]
    
    # 列表行
    elif line.strip().split('.')[0].isdigit():
        num, content = line.split('.', 1)
        line = num + '. ' + content.strip()
    elif line.strip()[1] != ' ':
        title = line.strip()[0]
        line = line.split(title, 1)[0] + title + ' ' + line.split(title, 1)[1]
    return line




def is_mark(line):
    # 判断这一行开头是否有特殊标记
    if line.startswith(('-', '*', '+', '>', '```', '|', ' ' * 4, '#')) \
            or not line.strip() or line.split('.')[0].isdigit() \
            or line.strip() in ("---", "===", "***", "* * *"):
        return True
    return False


# 这里为了加上换行将最后一块语句输出
def _yield_line(lines):
    for line in lines:
        yield line
    yield '\n'

# 这里为了处理额外插入的token
# 额外插入的token必须有一个类方法match, 用来判断该语句块是否符合这个token
def deal_extra_token(block_lines, extra_tokens):
    if not block_lines:
        return None
    for token in extra_tokens:
        if token.match(block_lines):
            return token(block_lines)