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
    Quote_Fence = False
    List_Fence = False
    Table_Fence = False
    Code_Fence = False
    for line in lines:
        line = line.replace('\t', ' ' * 4)
        if Quote_Fence:
            if line.startswith((" " * 4, ">")) == -1:
                Quote_Fence = False
                yield tokens["QuoteToken"](block_lines)
                block_lines.clear()
                block_lines.append(line)
            else:
                block_lines.append(insert_blank(line, ('>', )))
        elif List_Fence:
            if line.startswith(("-", "*", "+", " " * 4)) == -1:
                List_Fence = False
                yield tokens["ListToken"](block_lines)
                block_lines.clear()
                block_lines.append(line)
            else:
                block_lines.append(insert_blank(line, ('-', '*', '+')))
        elif Table_Fence:
            if line.startswith("|") == -1:
                Table_Fence = False
                yield tokens["TableToken"](block_lines)
                block_lines.clear()
            block_lines.append(line)

        elif Code_Fence:
            if line.startswith('```'):
                Code_Fence = False
                block_lines.append(line)
                yield tokens["BlockCodeToken"](block_lines)
                block_lines.clear()
            else:
                block_lines.append(line)

        elif line.find(("---", "===", "***", "* * *")):
            if line.strip() == "---" or "===" or "***" or "* * *":
                if block_lines:
                    block_lines.append(line)
                    yield tokens["HeadToken"](block_lines)
                    block_lines.clear()
                else:
                    yield tokens["SeparatorToken"](line)
        elif line.startswith("#"):
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
                line = ''.join(line[:index - 1]) + ' ' + ''.join(line[index:])
            yield tokens["HeadToken"](line)
        elif line.startswith(("- ", "* ", "+ ", ">")):
            if block_lines:
                yield tokens["ParagraphToken"](block_lines)
                block_lines.clear()
            if line[1] != ' ':
                line = line[0] + ' ' + ''.join(line[1:])
            block_lines.append(line)
            if line.startswith(">"):
                Quote_Fence = True
            else:
                List_Fence = True
        elif line.startswith("```"):
            if block_lines:
                yield tokens["ParagraphToken"](block_lines)
                block_lines.clear()
            block_lines.append(line)
            if line.startswith("|"):
                Table_Fence = True
            else:
                Code_Fence = True
        elif not line.strip():
            if block_lines:
                yield tokens["ParagraphToken"](block_lines)
                block_lines.clear()
        else:
            block_lines.append(line)

    def insert_blank(content, value):
        """
        判断list行和quote行符号后是否有正确的空格与内容隔开, 没有就加上
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
                continue
            if a_char in value:
                char_list.append(a_char)
                stage_1 = True
            else:
                # 开始cchar_list只可能会加几个空格, 所以我不需要清除char_list里的元素
                # 把content去掉前面的空格就好, 这样前面的空格会保留一次
                char_list.append(block_lines.pop() + content.strip() + "\n")
                break
        return ''.join(char_list)


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
