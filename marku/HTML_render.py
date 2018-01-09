#!/usr/bin/env python
# -*- coding: utf-8 -*-
__aythor__ = 'Aiyane'
import render
import html


class HTMLRenderer(render):
    """这是HTML的render, 即渲染各个token成HTML格式"""

    def __init__(self):
        """构造函数 """

    def StrongTokenRender(self, token):
        text = '<strong>{}</strong>'
        return text.format(self.render_line(token))

    def EmphasisTokenRender(self, token):
        text = '<em>{}</em>'
        return text.format(self.render_line(token))

    def EscapeCharTokenRender(self, token):
        return self.render_line(token)

    def InlineCodeTokenRender(self, token):
        text = '<code>{}</code>'
        return text.format(self.render_line(token))

    def DeleTokenRender(self, token):
        text = '<del>{}</del>'
        return text.format(self.render_line(token))

    def ImageTokenRender(self, token):
        text = '<img src="{}" title="{}" alt="{}">'
        inner = render_line(token)
        return text.format(token.src, token.title, inner)

    def LinkTokenRender(self, token):
        return

    def AutoLinkTokenRender(self, token):
        return

    def HeadTokenRender(self, token):
        return

    def QuoteTokenRender(self, token):
        return

    def BlockCodeTokenRender(self, token):
        return

    def SeparatorTokenRender(self, token):
        return

    def ListTokenRender(self, token):
        return

    def TableTokenRender(self, token):
        return

    def RawTextRender(self, token):
        return

    def ParagraphTokenRender(self, token):
        return

    def ListItemRender(self, token):
        return

    def TableRowRender(self, token):
        return

    def TableCellRender(self, token):
        return

    def DocumentTokenRender(self, token):
        return self.render_line(token)

