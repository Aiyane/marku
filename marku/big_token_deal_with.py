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

    # 这里为了处理额外插入的token
    # 额外插入的token必须有一个类方法match, 用来判断该语句块是否符合这个token
    def deal_extra_token():
        if not block_lines:
            return None
        for token in extra_tokens:
            if token.match(block_lines):
                return token(block_lines)

    for line in _yield_line(lines):
        line = line.replace('\t', ' ' * 4)
        if Quote_Fence or List_Fence:
            # 处理列表块或引用块
            # 这里的代码处理没有空行的能再识别接下来的语句块
            if not line.startswith(("-", "*", "+", ">", " " * 4)) and not line.split('.')[0].isdigit()\
                    and not (line.strip().startswith('>') and Quote_Fence):
                if Quote_Fence:
                    yield tokens["QuoteToken"](block_lines)
                else:
                    yield tokens["ListToken"](block_lines)
                block_lines.clear()
                List_Fence = Quote_Fence = False
            elif line.strip().split('.')[0].isdigit() and List_Fence:
                if not line.split('.')[1].startswith(' '):
                    line = line.split('.')[0] + '. ' + line.split('.')[1]
                block_lines.append(line)
                continue
            else:
                if line.strip().startswith('>') and Quote_Fence:
                    line = line.strip()
                # 这里将一行中可能没有空格的不标准的语法加上空格
                if line.strip()[1] != ' ':
                    title = line.strip()[0]
                    line = line.split(title, 1)[0] + title + " " + line.split(title, 1)[1]
                block_lines.append(line)
                continue
        elif Table_Fence:
            # 处理表格块
            # 这里的代码处理没有空行的能再识别接下来的语句块
            if not line.startswith("|"):
                Table_Fence = False
                yield tokens["TableToken"](block_lines)
                block_lines.clear()
            else:
                block_lines.append(line)
                continue
        elif Code_Fence:
            if line.startswith('```'):
                Code_Fence = False
                block_lines.append(line)
                yield tokens["BlockCodeToken"](block_lines)
                block_lines.clear()
            else:
                block_lines.append(line)
            continue
        elif Blank_Fence:
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
        token = deal_extra_token()
        if token:
            yield token
            block_lines.clear()
            if not is_mark(line):
                block_lines.append(line)
                continue
        else:
            if is_mark(line):
                yield init_token(block_lines)
                block_lines.clear()
            else:
                block_lines.append(line)
                continue

        if line.startswith("#"):
            # index是在那个位置开始就没有'#', 而且不是' '
            # 说明用户没有遵守语法标准
            # 我们需要在那个位置之后加上一个空格
            index = 0
            for char in line:
                if char != "#":
                    if char == ' ':
                        index = 0
                    break
                index += 1
            if index != 0:
                line = ''.join(line[:index]) + ' ' + ''.join(line[index:])
            yield tokens["HeadToken"]([line])
        elif line.strip() in ("---", "===", "***", "* * *"):
            # 说明是分隔符
            yield tokens["SeparatorToken"]([line.strip()])
        elif line.startswith(("-", "*", "+", ">")):
            if line[1] != ' ':
                line = line[0] + ' ' + ''.join(line[1:])
            block_lines.append(line)
            if line.startswith(">"):
                Quote_Fence = True
            else:
                List_Fence = True
        elif line.split('.')[0].isdigit():
            if not line.split('.')[1].startswith(' '):
                line = line.split('.')[0] + '. ' + line.split('.')[1]
            block_lines.append(line)
            List_Fence = True
        elif not line.strip():
            continue
        else:
            block_lines.append(line)
            if line.startswith("|"):
                Table_Fence = True
            elif line.startswith(' ' * 4):
                Blank_Fence = True
            else:
                Code_Fence = True


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
