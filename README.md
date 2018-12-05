# Marku

这里有一个渲染本文件夹中test2.md的[例子](https://qq2310091880.github.io/out "例子")

这是一个`Markdown`解释器, 通过解析出`Markdown`文件的语法树, 再利用语法树解析成`HTML`格式

## 目录

- [特点](#特点)
- [测试](#测试)
- [快速开始](#快速开始)
- [详细使用](#详细使用)
- [注意事项](#注意事项)

## 特点

1. 该包的特点是能够极大的容忍用户写的markdown文件的语法错误, test2.md是一个充满语法错误的markdown文件, 但是其渲染出来的结果与test.md基本一致.
2. 支持自定义标签的class, 代码高亮的开关
3. 支持自定义css样式, 支持在head头部添加代码块
4. 支持自定义的语法块以及语法块的具体处理

## 测试

`marku`文件夹为此包, `test.py` 是一个使用例子, 运行`python3 test.py`查看例子结果, `test.py2`是另一个例子, 运行`python3 test2.py {输入文件名} {输出文件名}`, 输入文件名为markdown文件, 输出为html文件

## 快速开始

该包支持自定义渲染css文件, 在head中添加其他代码(other), style.css是默认css样式, test.md是测试的markdown文件, 以下是使用例子, 默认使用`highlight.js`高亮代码

```py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Marku的简单使用
"""

from marku import Marku
import os
import webbrowser

loc = os.getcwd()

md = Marku(loc + "/test2.md")
md.render(loc + "/out.html")
webbrowser.open(loc + "/out.html")
```

运行完可以看到文件夹中出现`out.html`, 即为目标文件, 其中render接受三个参数, 第二个为自定义css渲染文件路径, 第三个为其他需要添加在head标签的代码字符串

## 详细使用

首先需要创建Marku对象

    from marku import Marku
    md = Marku('/home/aiyane/code/python/marku/test2.md')

同样可以在创建对象时加入自定义的css样式, 以及在head头部你希望写的代码

    code = '<style></style>'
    md = Marku('/home/aiyane/code/python/marku/test2.md', 'home/aiyane/style.css', code)

默认代码高亮是打开的, 也许你希望在head头部定义其他风格的代码高亮, 所以需要关闭默认高亮

    md = Marku('test2.md', css='style.css', other=code, highlight=False)

你可能需要添加自定义的标签class属性, 目前支持以下标签

    tokenClass = {
        "strongClass":      "strong",
        "emClass":          "em",
        "codeClass":        "code",
        "delClass":         "del",
        "imgClass":         "img",
        "aClass":           "a",
        "hClass":           "h",
        "blockquoteClass":  "quote",
        "preClass":         "pre",
        "tableClass":       "table",
        "pClass":           "p"
    }
    md.addClass(tokenClass)

也许你还想渲染其他特殊的语法块, 比如你想自定义语法, 例如你想以`...`中的文字表示特殊的语句块, 像以下

```
...
这里我自定义的
语法内容
...
```

这并不是markdown的语法, 但是你能用这个包来扩展语法, 你只需要新写一个文件例如`my_token.py`

```py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# my_token.py
from marku import big_token, little_token

__token__ = ['DotToken']
__func__ = ['DotTokenRender']

class DotToken(big_token.BaseBigToken):
    def __init__(self, lines):
        self.content = ''.join(lines[1:-1])
        super().__init__(self.content, little_token.deal_with_line)

    @staticmethod
    def match(lines):
        if len(lines) > 1 and lines[0].strip() == '...' and lines[-1].strip() == '...':
            return True
        return False

def DotTokenRender(render, token):
    # 如果你不希望按照markdow语法渲染你的结果, 那么就直接返回你需要的语法类的对象的内容也行
    # 如以下返回的是token.content, 就是上面的类的构造函数你保存的属性
    # return '<p>我的语法内容<br/>' + token.content + '</br>就在上面</p>'
    # 如果你需要markdown格式来渲染你的内容, 那么就调用渲染函数直接渲染语法类的对象, 如以下
    return '<p>我的语法内容<br/>' + render.render_line(token) + '</br>就在上面</p>'
```

这个自定义的语法为多行的语法, 并不是一行以内的语法, 所以DotToken需要继承big_token.BaseBigToken 在你定义的类中, 你的构造函数会接受一个参数, 这个参数是一个列表, 而且列表中的每一个元素就是每一行, 而且肯定是你语法块的那些行, 所以你可以对这个语法块进行你需要的任何处理, 在这个例子中只是将`...`之内的内容进行实例化.

在little_token中有deal_with_line方法, 这个方法会对多行语法中的内容按照markdown进行解析, 实例化的时候传入解析内容与这个函数即可, 即`super().__init__(content, little_token.deal_with_line)` 这一行

如果你定义的是一个跨越多行的语法块, 你必须定义一个**match**方法, 该方法必须是被@staticmethod装饰, 这个方法的作用是判断这个语句块是否符合你定义的语法, 可以看出, 只要第一行为`...`, 最后一行也为`...`, 那么就是符合语句的, 返回True, 否则返回False, 另外这个文件需要有一个全局变量`__token__`, 这是一个列表, 里面是你需要添加的语法类名.

你还需要定义一个处理内容的方法, 该方法的命名必须是**类名+Render**, 你必须接收的第一个参数为Marku对象的实例, 第二个参数为语法类的对象, 然后返回的就是html需要显示的内容. 使用方法可以参见注释.

最后添加自定义的语法块只需要进行如下:

```py
import my_token  # 你写的my_token.py文件

# ...
# 得到Marku对象md的一系列操作
md.add_extra(my_token)
```

仅仅简单调用`add_extra`函数你就添加了额外的语法处理了.如果你需要处理的是 *一行之中的语法* 例如在两个`!`之间也是强调内容

    这是一句话的!重点强调!的部分

上面中`!重点强调!`就是你定义的新语法, 那么还是在刚才的文件里, 加上以下内容即可添加新语法.

```py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# my_token.py
import re
from marku import little_token

__token__ = ['DotToken', 'NewToken']
__func__ = ['DotTokenRender', 'NewTokenRender']


class NewToken(little_token.BaseLittleToken):

    pattern = re.compile(r'\!(.+?)\!')

    def __init__(self, match_obj):
        self.content = match_obj.group(1)

def NewTokenRender(render, token):
    return '<em>' + token.content + '</em>'
```

与上面是类似的, 你需要建一个语法类, 不过这一次要继承little_token.BaseLittleToken 然后没有match函数了, 取而代之的是pattern变量, 它是一个正则, 用来匹配你的语法, 这里就是匹配前后带有`!`中间有内容的语法

在构造函数中接收的就是正则匹配的内容, 所以可以用group()函数来获取两个`!`之间的内容, 同样需要一个方法, 这里直接返回了加强调标签的字符串. 最后别忘了在`__token__`和`__func__`中注册.

**注意**: 对于自定义的**多行**语法块, 写Markdown文件时, 在新语法块前后可以没有空行, 也就是说新添加的语法块同样可以容忍用户的语法错误, 对于多行的匹配, 采取的是贪婪的匹配模式, 例如定义以下为语法块

    ...
    这是语法块, 在这个语法块中,
    必须用上下的三个'.'来包裹这个语法块
    ...

一般用户定义的语法块的match函数可能有多种情况都会判断成立, 例如以下

    ...
    这是语法块, 在这个语法块中,
    必须用上下的三个'.'来包裹这个语法块
    ...
    ...

在这里`前4行`与`前5行`都可以认为是正确的语法块, 用户定义的match函数并没有办法准确匹配的话, 那么这里会采用*前5行*, 因为匹配是贪婪的, 虽然这个包能容忍用户很多非换行的错误, 但是如果需要只匹配前4行, 那么写文件时**请注意换行** 工具并不是万能的 :)

最后的渲染就很简单了, 你可以输出成字符串

    html_str = md.render()

你也可以输出到文件

    md.render('/home/aiyane/output.html')

这样就可以在输出路径看到output.html了

关于语法的扩展, my_token.py是一个扩展的例子, 在test2.md中有扩展的语法, 运行`python3 test.py`可以查看结果

## 注意事项

注意事项中`<==>`代表渲染结果相等, `=>`代表渲染结果为, `()`括号中为例子注释

以下的例子渲染结果应该为相同的:

###### 在行头标志后没有空格

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

###### 所有语句块的缺失空行的错误是被允许的

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

**注意**: 不支持类似与代码块的多行自定义语法, 因为代码块中出现了markdown其他多行语法块, 是不会被识别渲染的, 可是自定义的语法块的优先级不会比Markdown原生语法高, 所以如果中间出现了markdown的多行语法块, 会优先渲染.例如:

```
...
## 标题
> 引用
> 引用
这是内容
...
```

类似于上述语法块, 在渲染时会将标题和引用渲染出来, 而不会将自定义的语法块渲染出来. 只会将`...`识别为一般的段落, 所以需要特别注意这一点.
