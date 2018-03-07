#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
这个文件用来处理块级语法的划分,  由于要满足以下目标, 所以代码由本来只渲染标准markdown语法的20行以内变成上百行, 真是悲伤的故事
目标:
    1. 容忍默认的markdown的块级语法中每一行可能出现的语法错误
    2. 容忍无论是markdown默认块级语法还是用户自定义的块级语法的无空行分割的错误
    3. 自定义块级语法按照贪婪匹配模式

使用说明中`<==>`代表渲染结果相等, `=>`代表渲染结果为, `()`括号中为例子注释

以下的例子渲染结果应该为相同的:

##### 在行头标志后没有空格

```
## 标题       <==>         ##标题
> 引用        <==>         >引用
> > 引用      <==>         >>引用   <==>    > >引用
- 列表        <==>         -列表
1. 列表       <==>         1.列表
```

###### 以下引用是等效的

```
> > > 引用
    > > >引用
>>>引用
> >>引用
>> >引用
    >>>引用(会被优先当成引用而不不是缩进代码)
(类似的其他空格错误)
```

###### 以下下划线被认为是相同的

```
---
 ---
  ---
    --- (会被优先当成下划线而不是缩进代码)
(类似的其他前有空格的错误)
```

###### 所有语句块的缺失空行的错误

```
## 标题
--- (下划线)
    缩进代码
    缩进代码
普通段落
|表格|表格|
|:---|:---:|
|表格|表格|
> 引用
> 引用
- 列表
- 列表
    1. 有序列表
    2. 有序列表
(其他块级语法与自定义块级语法)
```

###### 注意普通段落的换行并不会有效果, 只会是一个空格连接, 需要有空行才会分段

```
这是普通的一行             => 这是普通的一行 这里的换行并没有效果
这里的换行并没有效果
=========================================================
这是普通的一行
                            => 这是普通的一行
加上空行才是分段               加上空行才是分段
```

###### 注意以`*`开头的行, 可能会有以下三种意思, 所以必须以`* `(注意有一个空格)开始才是列表:

```
*这是斜体*
**这是粗体**
* 这是列表
```

###### 在缩进代码中的特殊语法只会被当成代码, 但是如果是以特殊语法开头则不是

```
---(前面有四个空格, 但是不是在缩进代码块中, 所以会被当成下划线)
> > > 引用(前面有四个空格, 但是不是在缩进代码块中, 所以会被当成引用)

这是代码块的开始
--- (会被当成代码)
> > > 引用(会被当成代码)
```

###### 贪婪的匹配模式:

```
例如自定义语法:
    ...
    这是三个'.'包围的语法
    ...
那么以下会被整体匹配, 而不是只匹配前三行:
    ...
    这是三个'.'包围的语法
    ...
    ...
```
"""
__author__ = "Aiyane"


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
        :save_token: 临时保存的token
    """
    block_lines = []
    Quote_Fence = False
    List_Fence = False
    Table_Fence = False
    Code_Fence = False
    Blank_Fence = False
    save_token = None

    # 倒序查找是否有符合的token
    def find_token(block_lines):
        """
        以最后一行为基准, 例如1至10行, 则判断1-10, 再判断2-10, 3-30, ...最后10
        当中有任意一段判断符合Token语法, 例如3-10符合, 就将1-2先以init_token的形式yield出
        再让3-10行yield出, 为什么不yield 3-10的token呢? 因为可能下一行会让3-11行也符合
        Token语法, 所以我们只会将token保存在save_token变量中, 不会直接在这个函数返回token
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
                nonlocal save_token
                save_token = token
                yield 1
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

        elif line.startswith(("-", "* ", "+", ">")):
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
            if line.startswith(("* ", "-", "+", " " * 4)) or line.split('.')[0].isdigit():
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
            if isinstance(token, int):
                block_lines.append(line)
                is_continue = True
                break
            yield token
        if is_continue:
            continue

        if save_token:
            yield save_token
            save_token = None
            first_line = block_lines[-1]
            scond_line = line
            block_lines.clear()

            if has_mark(first_line) and first_line.strip():
                # 第一行有标志的
                token = deal_mark_line(first_line)
                if token:
                    yield token
                token = deal_mark_tail_line(scond_line)
                if token and not isinstance(token, bool):
                    yield token
            elif first_line.strip():
                # 第一行没标志的
                block_lines.append(first_line)

        if has_mark(line):
            if block_lines:
                yield init_token(block_lines)
                block_lines.clear()
            if not line.strip():
                continue
            token = deal_mark_line(line)
            if token:
                yield token
        else:
            block_lines.append(line)


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
    if line.startswith(('-', '* ', '+', '>', '```', '|', ' ' * 4, '#')) or not line.strip() \
            or line.split('.')[0].isdigit() or line.strip() in ("---", "===", "***", "* * *"):
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
        yield lines[i + 1:], lines[0:i + 1]


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
