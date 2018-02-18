#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Aiyane'
"""
一个命令行脚本渲染markdown的例子
"""
import sys
import os
from marku import Marku
import my_token  # 自定义语法
import webbrowser

argv = sys.argv

try:
    input_file, output_file = argv[1], argv[2]
except Exception:
    print("请输入正确命令: 'python3 test2.py {输入文件路径} {输出文件路径}'")
    sys.exit()

if not os.path.isfile(input_file):
    print("打开文件出错, 请检查文件!")
    sys.exit()
md = Marku(input_file)
# 扩展语法
md.add_extra(my_token)
# 渲染结果
md.render(output_file)
webbrowser.open(output_file)
