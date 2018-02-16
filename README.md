# Marku

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
        - __init__.py
    - test.py
    - test2.py
    - style.css
    - test.md
    - .gitignore
    - README.md

## 测试

`marku`文件夹为此包, `test.py` 是一个使用例子, 运行`python3 test.py`查看例子结果, `test.py2`是另一个例子, 运行`python3 test2.py {输入文件名} {输出文件名}`, 输入文件名为markdown文件, 输出为html文件

## 说明

该包支持自定义渲染css文件, 代码高亮采用`highlight.js`, style.css是一个css文件例子, test.md是测试的markdown文件, 以下是test.py里的使用例子

```py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Marku的简单使用
"""

from marku import Marku
import os

loc = os.getcwd()

md = Marku(loc + "/test.md", loc + '/style.css')
md.render(loc + "/out.html")
```

运行完可以看到文件夹中出现`out.html`, 即为目标文件
