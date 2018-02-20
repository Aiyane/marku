#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Aiyane'
from marku import big_token
from marku import little_token
from marku import HTMLRenderer
from marku.HTML_token import HTMLBigToken, HTMLLittleToken


class Marku(HTMLRenderer):
    def __init__(self, input_file, css=None, other='', highlight=True):
        """
        input_file: 输入文件路径
        css_file: 输入css文件路径
        other: head标签的其他语句
        """
        self.highlight = highlight
        self.input_file = input_file
        self.css_file = css
        self.other = other
        self.css = ''

    def add_extra(self, extras):
        """
        这是一个扩展语法的方法
        extras: 自定义语法的模块, 即文件名
        """
        self._extras = extras
        funcs = self._getfunc(extras)
        self._add_funcs(funcs)

    def _getfunc(self, extras):
        """
        获得额外func
        """
        return [getattr(extras, func_name) for func_name in extras.__func__]

    def _add_funcs(self, funcs):
        """
        增加额外的处理方法
        """
        for func in funcs:
            setattr(self, func.__name__, func)

    def addClass(self, cls_dict=None):
        """
        这是一个给标签增加class属性的方法
        cls_dict: 增加的class属性值
        """
        from marku.HTML_class import addClass
        self._token_class = addClass(cls_dict)

    def _add_tokens(self, tokens):
        """
        增加额外的tokens
        """
        super(Marku, self).__init__(*tokens)
        for token in tokens:
            if hasattr(token, 'match'):
                big_token.add_token(token)
            else:
                little_token.add_token(token)

    def render(self, output_file=None):
        """
        output_file: 输出文件路径
        """

        try:
            with open(self.input_file, 'r', encoding="utf8") as fin:
                big_token.add_token(HTMLBigToken)
                little_token.add_token(HTMLLittleToken)
                if hasattr(self, '_extras'):
                    tokens = self._get_tokens(self._extras)
                    self._add_tokens(tokens)
                else:
                    super(Marku, self).__init__()
                AST = big_token.DocumentToken(fin)
            if self.css_file is not None:
                with open(self.css_file, 'r', encoding="utf8") as f:
                    self.css = f.read()
        except IOError:
            print("打开文件出错, 请检查文件!")

        rendered = self.rendered(AST, self.css, self.other, self.highlight)
        if output_file is None:
            return rendered
        try:
            with open(output_file, 'w') as f:
                f.write(rendered)
            print("文件已渲染完毕!")
        except IOError:
            raise NotADirectoryError('输出路径不存在!')
