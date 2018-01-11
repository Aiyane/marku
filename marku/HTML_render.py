#!/usr/bin/env python
# -*- coding: utf-8 -*-
__aythor__ = 'Aiyane'
from render import BaseRender
import html
import HTML_token
from itertools import chain
from HTML_class import tokenClass

class HTMLRenderer(BaseRender):
    """这是HTML的render, 即渲染各个token成HTML格式"""

    def __init__(self, *extras):
        """构造函数 """
        HTMLToken = self._get_tokens(HTML_token)
        super().__init__(*chain(HTMLToken, extras))

    def StrongTokenRender(self, token):
        text = '<strong class="{strongClass}">{}</strong>'
        return text.format(tokenClass['strongClass'] ,self.render_line(token))

    def EmphasisTokenRender(self, token):
        text = '<em class="{emClass}">{}</em>'
        return text.format(tokenClass['emClass'], self.render_line(token))

    def EscapeCharTokenRender(self, token):
        return self.render_line(token)

    def InlineCodeTokenRender(self, token):
        text = '<code class="{codeClass}">{}</code>'
        return text.format(tokenClass['codeClass'], self.render_line(token))

    def DeleTokenRender(self, token):
        text = '<del class="{delClass}">{}</del>'
        return text.format(tokenClass['delClass'], self.render_line(token))

    def ImageTokenRender(self, token):
        text = '<img class="{imgClass}" src="{}" title="{}" alt="{}">'
        inner = self.render_line(token)
        return text.format(tokenClass['imgClass'], token.src, token.title, inner)

    def LinkTokenRender(self, token):
        text = '<a class="{aClass}" href="{target}">{inner}</a>'
        target = escape_url(token.target)
        inner = self.render_line(token)
        return text.format(tokenClass['aClass'], target=target, inner=inner)

    def AutoLinkTokenRender(self, token):
        text = '<a class="{aClass}" href="{target}">{inner}</a>'
        target = escape_url(token.target)
        inner = self.render_line(token)
        return text.format(tokenClass['aClass'], target=target, inner=inner)

    def HeadTokenRender(self, token):
        text = '<h{level} class="{hClass}">{inner}</h{level}>\n'
        inner = self.render_line(token)
        return text.format(tokenClass['hClass'], level=token.level, inner=inner)

    def QuoteTokenRender(self, token):
        text = '<blockquote class="{blockquoteClass}">\n{inner}</blockquote>\n'
        return text.format(tokenClass['blockquoteClass'], inner=self.render_line(token))

    def BlockCodeTokenRender(self, token):
        text = '<pre class="{preClass}">\n<code{attr}>\n{inner}</code>\n</pre>\n'
        if token.language:
            attr = 'class="{}"'.format('lang-{}'.format(token.language))
        else:
            attr = ''
        inner = self.render_line(token)
        return text.format(tokenClass['preClass'], attr=attr, inner=inner)

    def SeparatorTokenRender(self, token):
        return '<hr>\n'

    def ListTokenRender(self, token):
        text = '<{tag}{attr}>\n{inner}</{tag}>\n'
        if token.start:
            tag = 'ol'
            attr = ' start="{}"'.format(token.start)
        else:
            tag = 'ul'
            attr = ''
        inner = self.render_line(token)
        return text.format(tag=tag, attr=attr, inner=inner)

    def TableTokenRender(self, token):
        text = '<table class="{tableClass}">\n{inner}</table>\n'
        if token.has_header:
            head_text = '<thead>\n{inner}</thead>\n'
            header = token.kids[0]
            head_inner = self.TableRowRender(header, True)
            head_rendered = head_text.format(inner=head_inner)
        else:
            head_rendered = ''
        body_text = '<tbody>\n{inner}</tbody>\n'
        body_inner = self.render_line(token)
        body_rendered = body_text.format(inner=body_inner)
        return text.format(tokenClass['tableClass'], inner=head_rendered + body_rendered)

    def RawTextRender(self, token):
        return html.escape(token.content)

    def ParagraphTokenRender(self, token):
        return '<p class="{pClass}">{}</p>\n'.format(tokenClass['pClass'], self.render_line(token))

    def ListItemRender(self, token):
        return '<li>{}</li>\n'.format(self.render_line(token))

    def TableRowRender(self, token, is_header=False):
        if not is_header and token.header:
            return ""
        text = '<tr>\n{inner}</tr>\n'
        inner = ''.join(
            [self.TableCellRender(kid, is_header) for kid in token.kids])
        return text.format(inner=inner)

    def QuoteItemRender(self, token):
        return '{}<br>'.format(self.render_line(token))

    def HTMLBigTokenRender(self, token):
        return token.content

    def HTMLLittleTokenRender(self, token):
        return token.content

    def TableCellRender(self, token, in_header=False):
        text = '<{tag}{attr}>{inner}</tag>\n'
        tag = 'th' if in_header else 'td'
        if token.align == 0:
            align = 'left'
        elif token.align == 1:
            align = 'center'
        elif token.align == 2:
            align = 'right'
        attr = ' align="{}"'.format(align)
        inner = self.render_line(token)
        return text.format(tag=tag, attr=attr, inner=inner)

    def DocumentTokenRender(self, token):
        return self.render_line(token)


def escape_url(raw):
    """
    进行url编码
    """
    from urllib.parse import quote
    return quote(raw, safe='/#:')
