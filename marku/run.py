#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Aiyane'
import sys
import big_token
import little_token
from HTML_render import HTMLRenderer
from HTML_token import HTMLBigToken, HTMLLittleToken

argv = sys.argv

try:
    input_file, output_file = argv[1], argv[2]
except Exception:
    print("请输入正确命令, python run.py \{输入文件名\} \{输出文件名\}")
try:
    with open(input_file, 'r', encoding="utf8") as fin:
        big_token.add_token(HTMLBigToken)
        little_token.add_token(HTMLLittleToken)
        AST = big_token.DocumentToken(fin)
except Exception:
    print("打开文件出错, 请检查文件!")
rendered = HTMLRenderer(AST)
with open(output, 'w') as f:
    f.write(rendered)
