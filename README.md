# Marku

这里有一个渲染本文件夹中test2.md的[例子](https://qq2310091880.github.io/out "例子")

这是一个`Markdown`解释器, 一个自己练手的小项目, 打算解析出`Markdown`文件的抽象语法树, 再利用抽象语法树解析成`HTML`格式

## 目录

目前已完成一部分功能, 下载源码后, 打开源码文件夹到主目录下, 即 `marku-master` 目录. 这是的文件目录结构如下

- marku-master
    - marku
        - HTML_render.py
        - HTML_token.py
        - HTML_class.py
        - big_token.py
        - big_token_deal_with.py
        - little_token.py
        - little_token_deal_with.py
        - render.py
        - run.py
        - style.css
        - `__init__.py`
    - test.py
    - test2.py
    - test.md
    - test2.md
    - .gitignore
    - README.md

## 测试

`marku`文件夹为此包, `test.py` 是一个使用例子, 运行`python3 test.py`查看例子结果, `test.py2`是另一个例子, 运行`python3 test2.py {输入文件名} {输出文件名}`, 输入文件名为markdown文件, 输出为html文件

## 简单使用

该包支持自定义渲染css文件, 在head中添加其他代码(other), style.css是默认css样式, test.md是测试的markdown文件, 以下是test.py里的使用例子, 默认使用`highlight.js`高亮代码

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

### 特点

1. 该包的特点是能够极大的容忍用户写的markdown文件的语法错误, test2.md是一个充满语法错误的markdown文件, 但是其渲染出来的结果与test.md基本一致.
2. 支持自定义标签的class
3. 支持自定义css样式, 支持在head头部添加代码块
4. 支持自定义的语法块以及语法块的具体处理

### 详细使用

首先需要创建Marku对象

    from marku import Marku
    md = Marku('/home/aiyane/code/python/marku/test2.md')

同样可以在创建对象时加入自定义的css样式, 以及在head头部你希望写的代码

    code = '<style></style>'
    md = Marku('/home/aiyane/code/python/marku/test2.md', 'home/aiyane/style.css', code)

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
from marku import big_token

__token__ = ['DotToken']
__func__ = ['DotTokenRender']

class DotToken(big_token.BaseBigToken):
    def __init__(self, lines):
        self.content = ''.join(lines[1:-1])

    @staticmethod
    def match(lines):
        if lines[0].strip() == '...' and lines[-1] == '...':
            return True
        return False

def DotTokenRender(token):
    return '<p>我的语法内容<br/>' + token.content + '</br>就在上面</p>'
```

这个自定义的语法为多行的语法, 并不是一行以内的语法, 所以DotToken需要继承big_token.BaseBigToken 在你定义的类中, 你的构造函数会接受一个参数, 这个参数是一个列表, 而且列表中的每一个元素就是每一行, 而且肯定是你语法块的那些行, 所以你可以对这个语法块进行你需要的任何处理, 在这个例子中只是保存`...`之内的内容为一个属性.

如果你定义的是一个跨越多行的语法块, 你必须定义一个**match**方法, 该方法必须是被@staticmethod装饰, 这个方法的作用是判断这个语句块是否符合你定义的语法, 可以看出, 只要第一行为`...`, 最后一行也为`...`, 那么就是符合语句的, 返回True, 否则返回False, 另外这个文件需要有一个全局变量`__token__`, 这是一个列表, 里面是你需要添加的语法类名.

你还需要定义一个处理内容的方法, 该方法的命名必须是**类名+Render**, 你会接收一个语法类的对象, 然后返回的就是html需要显示的内容. 最后使用如下

    import my_token

    ...# 得到Marku对象md的一系列操作
    md.add_extra(my_token)

仅仅简单调用add_extra函数你就添加了额外的语法处理了.如果你需要处理的是一行之中的语法例如在两个`!`之间也是强调内容

    这是一句话的!重点强调!的部分

上面中`!重点强调!`就是你定义的新语法, 那么还是在刚才的文件里, 加上以下内容即可添加新语法.

```py
import re
from marku import little_token

__token__ = ['DotToken', 'NewToken']
__func__ = ['DotTokenRender', 'NewTokenRender']


class NewToken(little_token.BaseLittleToken):

    pattern = re.compile(r'\!(.+?)\!')

    def __init__(self, match_obj):
        self.content = match_obj.group(1)

def NewTokenRender(token):
    return '<em>' + token.content + '</em>'
```

与上面是类似的, 你需要建一个语法类, 不过这一次要继承little_token.BaseLittleToken 然后没有match函数了, 取而代之的是pattern变量, 它是一个正则, 用来匹配你的语法, 这里就是匹配前后带有`!`中间有内容的语法

在构造函数中接收的就是正则匹配的内容, 所以可以用group()函数来获取两个`!`之间的内容, 同样需要一个方法, 这里直接返回了加强调标签的字符串. 最后别忘了在`__token__`和`__func__`中注册.

最后的渲染就很简单了, 你可以输出成字符串

    html_str = md.render()

你也可以输出到文件

    md.render('/home/aiyane/output.html')

这样就可以在输出路径看到output.html了
