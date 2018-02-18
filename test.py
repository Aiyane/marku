#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Marku的简单使用
为渲染的html标签添加class属性值
"""

from marku import Marku
import os
import webbrowser

loc = os.getcwd()

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


def main():
    md = Marku(loc + "/test2.md")
    md.addClass(tokenClass)
    md.render(loc + "/out.html")
    webbrowser.open(loc + "/out.html")


if __name__ == '__main__':
    main()
