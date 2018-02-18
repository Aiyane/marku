#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Aiyane'
from marku.HTML_class import getClass


class BaseRender(object):
    """基础的render类
    如果你要解析成你需要的格式需要有以下规则
    首先你的自定义的render必须继承于BaseRender类
    然后你处理抽象语法树中的Token需要自定义处理函数, 函数的名字必须是
    'Token名'+'Render',例如'ListTokenRender'
    """

    def __init__(self, *extras):
        """构造函数"""
        self.render_map = {
            'StrongToken':      self.StrongTokenRender,
            'EmphasisToken':    self.EmphasisTokenRender,
            'EscapeCharToken':  self.EscapeCharTokenRender,
            'InlineCodeToken':  self.InlineCodeTokenRender,
            'DeleToken':        self.DeleTokenRender,
            'ImageToken':       self.ImageTokenRender,
            'LinkToken':        self.LinkTokenRender,
            'AutoLinkToken':    self.AutoLinkTokenRender,
            'HeadToken':        self.HeadTokenRender,
            'QuoteToken':       self.QuoteTokenRender,
            'BlockCodeToken':   self.BlockCodeTokenRender,
            'SeparatorToken':   self.SeparatorTokenRender,
            'ListToken':        self.ListTokenRender,
            'TableToken':       self.TableTokenRender,
            'RawText':          self.RawTextRender,
            'ParagraphToken':   self.ParagraphTokenRender,
            'ListItem':         self.ListItemRender,
            'TableRow':         self.TableRowRender,
            'TableCell':        self.TableCellRender,
            'QuoteItem':        self.QuoteItemRender,
            'DocumentToken':    self.DocumentTokenRender
        }
        self._extras = extras
        for token in extras:
            func = getattr(self, token.__name__ + 'Render')
            self.render_map[token.__name__] = func

    def _render(self, token):
        """
        render入口
        """
        return self.render_map[token.__class__.__name__](token)

    def rendered(self, token, css='', other=''):
        import os
        if css == '':
            with open(os.path.dirname(os.path.realpath(__file__)) + '/style.css', 'r', encoding='utf8') as f:
                css = f.read()
        content = """<!doctype html>
        <html><head><meta charset="utf-8">
        <link rel="stylesheet"
            href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@9.12.0/build/styles/default.min.css">
        <script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@9.12.0/build/highlight.min.js"></script>
        <script >hljs.initHighlightingOnLoad();</script>
        {other}
        <style>{css}</style>
        </head><body id="container" class="export export-html">
        """.format(css=css, other=other)
        content += self._render(token)
        content += """
        </body></html>
        """
        return content

    def render_line(self, token):
        """
        递归调用子Token
        """
        rendered = [self._render(kid) for kid in token.kids]
        return ''.join(rendered)

    def tokenClass(self, name):
        if not hasattr(self, '_token_class'):
            return getClass(name)
        return self._token_class[name]

    def addClass(self, cls_dict=None):
        from marku.HTML_class import addClass
        self._token_class = addClass(cls_dict)

    @staticmethod
    def _get_tokens(module):
        return [getattr(module, token_name) for token_name in module.__token__]
