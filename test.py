#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Marku的简单使用
为渲染的html标签添加class属性值
扩展文件my_token中的语法
"""
import my_token
from marku import Marku
import os
# import webbrowser  # 打开浏览器
from flask import Flask
app = Flask(__name__)

# 获得当前路径
# loc = os.getcwd()

# 扩展html标签的class属性值
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


@app.route('/')
def main():
    md = Marku("test2.md")
    # 增加class属性值
    md.addClass(tokenClass)
    # 增加自定义语法
    md.add_extra(my_token)
    # 渲染输出
    return md.render()
    # 浏览器打开
    # webbrowser.open(loc + "/out.html")


if __name__ == '__main__':
    app.run()
