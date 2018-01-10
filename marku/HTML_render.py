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
        text = '<a href="{target}">{inner}</a>'
        target = escape_url(token.target)
        inner = self.render_line(token)
        return text.format(target=target, inner=inner)

    def AutoLinkTokenRender(self, token):
        text = '<a href="{target}">{inner}</a>'
        target = escape_url(token.target)
        inner = self.render_line(token)
        return text.format(target=target, inner=inner)

    def HeadTokenRender(self, token):
        text = '<h{level}>{inner}</h{level}>\n'
        inner = self.render_line(token)
        return text.format(level=token.level, inner=inner)

    def QuoteTokenRender(self, token):
        text = '<blockquote>\n{inner}</blockquote>\n'
        return text.format(inner=self.render_line(token))

    def BlockCodeTokenRender(self, token):
        text = '<pre>\n<code{attr}>\n{inner}</code>\n</pre>\n'
        if token.language:
            attr = 'class="{}"'.format('lang-{}'.format(token.language))
        else:
            attr = ''
        inner = self.render_line(token)
        return text.format(attr=attr, inner=inner)

    @staticmethod
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
        text = '<table>\n{inner}</table>\n'
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
        return text.format(inner=head_rendered + body_rendered)

    def RawTextRender(self, token):
        return html.escape(token.content)

    def ParagraphTokenRender(self, token):
        return '<p>{}</p>\n'.format(self.render_line(token))

    def ListItemRender(self, token):
        return '<li>{}</li>\n'.format(self.render_line(token))

    def TableRowRender(self, token, is_header=False):
        if not is_header and token.header:
            return ""
        text = '<tr>\n{inner}</tr>\n'
        inner = ''.join(
            [self.TableCellRender(kid, is_header) for kid in token.kids])
        return text.format(inner=inner)

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
