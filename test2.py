#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Aiyane'
"""
一个命令行脚本渲染markdown的例子
"""
import sys
from marku import big_token
from marku import little_token
from marku import HTMLRenderer
from marku.HTML_token import HTMLBigToken, HTMLLittleToken
import webbrowser

argv = sys.argv

try:
    input_file, output_file = argv[1], argv[2]
except Exception:
    print("请输入正确命令, python3 test.py {输入文件名} {输出文件名}")
    sys.exit()
try:
    with open(input_file, 'r', encoding="utf8") as fin:
        big_token.add_token(HTMLBigToken)
        little_token.add_token(HTMLLittleToken)
        AST = big_token.DocumentToken(fin)
except IOError:
    print("打开文件出错, 请检查文件!")
    sys.exit()

rendered = HTMLRenderer().rendered(AST)
with open(output_file, 'w') as f:
    f.write(rendered)
print("文件已渲染完毕, 请在文件夹中检查输出文件")
webbrowser.open(output_file)
