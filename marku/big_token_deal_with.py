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

    def insert_blank(content, value):
        """
        判断list行和quote行符号后是否有正确的空格与内容隔开, 没有就加上
        char_list: 字符列表
        stage_1表明已经遇见行头的特殊标志符号
        stage_2表明标志符号后就是一个空格, 这说明这一行是符合标准语法的
        """
        char_list = []
        stage_1 = False
        stage_2 = False
        for a_char in content:
            if not stage_2 and stage_1:
                # 到了阶段1, 阶段2就会马上到
                if a_char != ' ':
                    char_list.append(' ')
                stage_2 = True
            if stage_2 or a_char == ' ':
                char_list.append(a_char)
            elif a_char in value:
                # 判断行头
                char_list.append(a_char)
                stage_1 = True
            else:
                # 开始char_list只可能会加几个空格, 所以我不需要清除char_list里的元素
                # 把content去掉前面的空格就好, 这样前面的空格会保留一次
                # block_lines.pop()会把最后一行抛出来， 拼在这一行
                char_list.append(block_lines.pop() + content.strip() + "\n")
                break
        return ''.join(char_list)

    # 这里为了处理额外插入的token
    # 额外插入的token必须有一个类方法match, 用来判断该语句块是否符合这个token
    def deal_extra_token(lines):
        for token in extra_tokens:
            if token.match(lines):
                return token(lines)
        return None

    # 这里为了加上换行将最后一块语句输出
    def _yield_line(lines):
        for line in lines:
            yield line
        yield '\n'

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
                if not line.strip():
                    # 如果是空行, 例如'\n'就直接读取下一行
                    continue
                # 如果不是空行, 会直接继续if语句判断这一行的标志
            elif line.strip().split('.')[0].isdigit() and List_Fence:
                if not line.split('.')[1].startswith(' '):
                    line = line.split('.')[0] + '. ' + line.split('.')[1]
                block_lines.append(line)
                continue
            else:
                if line.strip().startswith('>') and Quote_Fence:
                    line = line.strip()
                block_lines.append(insert_blank(line, ('-', '*', '+', '>')))
                continue
        elif Table_Fence:
            # 处理表格块
            # 这里的代码处理没有空行的能再识别接下来的语句块
            if not line.startswith("|"):
                Table_Fence = False
                yield tokens["TableToken"](block_lines)
                block_lines.clear()
                if not line.strip():
                    # 如果是空行, 例如'\n'就直接读取下一行
                    continue
                # 如果不是空行, 会直接继续if语句判断这一行的标志
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
        if line.strip() in ("---", "===", "***", "* * *"):
            if block_lines:
                # 说明是标题
                block_lines.append(line)
                yield tokens["HeadToken"](block_lines)
                block_lines.clear()
            else:
                # 说明是分隔符
                yield tokens["SeparatorToken"]([line])
        elif line.startswith("#"):
            if block_lines:
                # 这里说明是前面段落没有空行
                token = deal_extra_token(block_lines)
                if token:
                    yield token
                else:
                    yield init_token(block_lines)
                block_lines.clear()
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
        elif line.startswith(("-", "*", "+", ">")):
            if block_lines:
                # 这里说明前面段落没有空行
                token = deal_extra_token(block_lines)
                if token:
                    yield token
                else:
                    yield init_token(block_lines)
                block_lines.clear()
            if line[1] != ' ':
                line = line[0] + ' ' + ''.join(line[1:])
            block_lines.append(line)
            if line.startswith(">"):
                Quote_Fence = True
            else:
                List_Fence = True
        elif line.startswith("```") or line.startswith("|") or line.startswith(' ' * 4):
            if block_lines:
                # 这里说明前面段落没有空行
                token = deal_extra_token(block_lines)
                if token:
                    yield token
                else:
                    yield init_token(block_lines)
                block_lines.clear()
            block_lines.append(line)
            if line.startswith("|"):
                Table_Fence = True
            elif line.startswith(' ' * 4):
                Blank_Fence = True
            else:
                Code_Fence = True
        elif line.split('.')[0].isdigit():
            if block_lines:
                # 这里说明前面段落没有空行
                token = deal_extra_token(block_lines)
                if token:
                    yield token
                else:
                    yield init_token(block_lines)
                block_lines.clear()
            if not line.split('.')[1].startswith(' '):
                line = line.split('.')[0] + '. ' + line.split('.')[1]
            block_lines.append(line)
            List_Fence = True
        elif not line.strip():
            # 为了处理额外插入的token
            # 如果没有匹配上, 就返回默认token
            if block_lines:
                token = deal_extra_token(block_lines)
                if token:
                    yield token
                else:
                    yield init_token(block_lines)
                block_lines.clear()
        else:
            block_lines.append(line)
