#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Aiyane'
from marku import big_token
from marku import little_token
from marku import HTMLRenderer
from marku.HTML_token import HTMLBigToken, HTMLLittleToken


class Marku(object):
    def __init__(self, input_file, css_file=None):
        """
        input_file: 输入文件路径
        css_file: 输入css文件路径
        """
        self.input_file = input_file
        self.css_file = css_file
        self.css = ''

    def render(self, output_file=None):
        """
        output_file: 输出文件路径
        """
        try:
            with open(self.input_file, 'r', encoding="utf8") as fin:
                big_token.add_token(HTMLBigToken)
                little_token.add_token(HTMLLittleToken)
                AST = big_token.DocumentToken(fin)
            if self.css_file is not None:
                with open(self.css_file, 'r', encoding="utf8") as f:
                    self.css = f.read()
        except IOError:
            print("打开文件出错, 请检查文件!")

        rendered = HTMLRenderer().rendered(AST, self.css)
        if output_file is None:
            return rendered
        try:
            with open(output_file, 'w') as f:
                f.write(rendered)
            print("文件已渲染完毕!")
        except IOError:
            raise NotADirectoryError('输出路径不存在!')
