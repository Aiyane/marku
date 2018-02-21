#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Aiyane"
import debug


def init_deal_with(lines, tokenList, tokens, init_token, root=None):
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
    wait_next = None

    # 倒序查找是否有符合的token
    def find_token(block_lines):
        """
        以最后一行为基准, 例如1至10行, 则判断1-10, 再判断2-10, 3-30, ...最后10
        当中有任意一段判断符合Token语法, 例如3-10符合, 就将1-2先以init_token的形式yield出
        再让3-10行yield出, 为什么不yield 3-10的token呢? 因为可能下一行会让3-11行也符合
        Token语法, 所以我们只会将token保存在wait_next变量中, 不会直接在这个函数返回token
        记得我们的目标是 **贪婪匹配**
        参数:
            :block_lines: 判断的多行列表
            :lines: 以最后一行为基准的多行列表, 例如1-10行, 2-10行, 3-10行 ...
            :_lines: 以第一行为基准的多行, 例如1行, 1-2行, 2-3行 ...
            _lines + lines == block_lines
        """
        for lines, _lines in popList(block_lines):
            token = deal_extra_token(lines, tokenList)
            if token:
                for _token in _find_token(tokenList, init_token, _lines):
                    yield _token
                nonlocal wait_next
                wait_next = token
                yield lines
                break

    def deal_mark_line(line):
        nonlocal Quote_Fence
        nonlocal List_Fence
        nonlocal Blank_Fence
        nonlocal Table_Fence
        nonlocal Code_Fence
        if line.startswith("#"):
            # 处理标题
            line = line_deal(line)
            return tokens["HeadToken"]([line])

        elif line.strip() in ("---", "===", "***", "* * *"):
            # 说明是分隔符
            return tokens["SeparatorToken"]([line.strip()])

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


        else:
            block_lines.append(line)
            if line.startswith("|"):
                Table_Fence = True
            elif line.startswith(' ' * 4):
                Blank_Fence = True
            else:
                Code_Fence = True

    def deal_mark_tail_line(line):
        nonlocal List_Fence
        nonlocal Quote_Fence
        nonlocal Table_Fence
        nonlocal Code_Fence
        nonlocal Blank_Fence
        if List_Fence:
            # 列表
            if line.startswith(("*", "-", "+", " "*4)) or line.split('.')[0].isdigit():
                line = line_deal(line)
                block_lines.append(line)
                return None
            else:
                List_Fence = False
                return tokens['ListToken'](block_lines)

        elif Quote_Fence:
            # 引用
            if line.strip().startswith('>'):
                line = line_deal(line)
                block_lines.append(line)
                return None
            else:
                Quote_Fence = False
                return tokens['QuoteToken'](block_lines)

        elif Table_Fence:
            # 处理表格块
            # 这里的代码处理没有空行的能再识别接下来的语句块
            if line.startswith("|"):
                block_lines.append(line)
                return None
            else:
                Table_Fence = False
                return tokens["TableToken"](block_lines)

        elif Code_Fence:
            # ```开头的代码块
            if line.startswith('```'):
                Code_Fence = False
                block_lines.append(line)
                return tokens["BlockCodeToken"](block_lines)
            else:
                block_lines.append(line)

        elif Blank_Fence:
            # 空格开头的代码块
            if line.startswith(' ' * 4):
                block_lines.append(line)
                return None
            else:
                Blank_Fence = False
                return tokens['BlockCodeToken'](block_lines)
        else:
            return True

    for line in _yield_line(lines):
        line = line.replace('\t', ' ' * 4)
        token = deal_mark_tail_line(line)
        if not token:
            continue
        if not isinstance(token, bool):
            yield token
            block_lines.clear()
            if isinstance(token, tokens['BlockCodeToken']):
                continue

        # ================================================
            # 这一段的目地是为了进行额外的语法块匹配, 注意是贪婪匹配
            # 参数:
            #     :is_continue: 对外层循环的continue
        is_continue = False
        for token in find_token(block_lines):
            # 进行贪婪匹配, 如果匹配到的token是以最后一行为基准的
            # 那么token会返回一个list类型, 这时候需要贪婪的读取下一行
            # 再进行匹配, 如果没有匹配到, 就返回刚刚匹配的token(wait_next)
            # 再将没有用到的新line加到block_lines中
            if isinstance(token, list):
                block_lines.append(line)
                is_continue = True
                break
            elif token:
                yield token
        if is_continue:
            continue
        if wait_next:
            yield wait_next
            wait_next = None
            first_line = block_lines[-1]
            scond_line = line
            block_lines.clear()
            if has_mark(first_line) and first_line.strip():
                token = deal_mark_line(first_line)
                if token:
                    yield token
                token = deal_mark_tail_line(scond_line)
                if not token:
                    continue
                if not isinstance(token, bool):
                    yield token
                    block_lines.clear()
            else:
                if has_mark(scond_line):
                    yield init_token(first_line)
                    if not scond_line.strip():
                        continue
                    token = deal_mark_line(scond_line)
                    if token:
                        yield token
                        continue
                else:
                    block_lines.append(first_line)
                    # block_lines.append(scond_line)
        if not has_mark(line):
            block_lines.append(line)
            continue
        elif block_lines:
            yield init_token(block_lines)
            block_lines.clear()
        # =================================================

        if not line.strip():
            # 空行
            continue
        else:
            token = deal_mark_line(line)
            if token:
                yield token



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




def has_mark(line):
    # 判断这一行开头是否有特殊标记
    if line.startswith(('-', '*', '+', '>', '```', '|', ' ' * 4, '#')) \
            or not line.strip() or line.split('.')[0].isdigit() \
            or line.strip() in ("---", "===", "***", "* * *"):
        return True
    return False


def _yield_line(lines):
    # 这里为了加上换行将最后一块语句输出
    for line in lines:
        yield line
    yield '\n'
    yield '\n'

def deal_extra_token(block_lines, tokenList):
    # 这里为了处理额外插入的token
    # 额外插入的token必须有一个类方法match, 用来判断该语句块是否符合这个token
    if not block_lines:
        return None
    for token in tokenList:
        if token.match(block_lines):
            return token(block_lines)

def popList(lines):
    """
    参数:
        :lines: 多行列表
    返回例如:
        1-10, None
        2-10, 1
        3-10, 1-2
        4-10, 1-3
        ...
        None, 1-10
    """
    if not lines:
        return None
    length = len(lines)
    yield lines, None
    for i in (range(length)):
        if i == length - 1:
            yield None, lines[0:i]
        yield lines[i+1:], lines[0:i+1]

def _find_token(tokenList, init_token, lines):
    """
    与find_token函数的区别是, 如果一次都没匹配到, 默认返回init_token类型
    因为这个函数是第二重递归的函数, 所以可以直接返回init_token类型, 最外层需要
    进行贪婪匹配, 但是进入这个函数的lines就说明不是最外层.
    参数:
        :tokenList: Token的类的列表
        :init_token: 默认的Token
        :lines: 多行
    """
    for tail, pre in popList(lines):
        token = deal_extra_token(tail, tokenList)
        if token:
            for _token in _find_token(tokenList, init_token, pre):
                yield _token
            yield token
    else:
        if lines:
            yield init_token(lines)
