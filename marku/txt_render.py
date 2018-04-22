#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
# txt_render.py
__aythor__ = 'Aiyane'
from marku.render import BaseRender
import html
from marku import HTML_token
from itertools import chain


class TxtRender(BaseRender):
    """这是HTML的render, 即渲染各个token成HTML格式"""

    def __init__(self, *extras):
        """构造函数 """
        HTMLToken = self._get_tokens(HTML_token)
        super().__init__(*chain(HTMLToken, extras))

    @staticmethod
    def StrongTokenRender(self, token):
        text = '<strong>**{}**</strong>'
        return text.format(self.render_line(token))

    @staticmethod
    def EmphasisTokenRender(self, token):
        text = '<em>*{}*</em>'
        return text.format(self.render_line(token))

    @staticmethod
    def EscapeCharTokenRender(self, token):
        return self.render_line(token)

    @staticmethod
    def InlineCodeTokenRender(self, token):
        text = '<code>`{}`</code>'
        return text.format(self.render_line(token))

    @staticmethod
    def DeleTokenRender(self, token):
        text = '<del>~~{}~~</del>'
        return text.format(self.render_line(token))

    @staticmethod
    def ImageTokenRender(self, token):
        text = '<span style="color: bule;">![{}]({}&nbsp;"{}")</span><br>'
        inner = self.render_line(token)
        return text.format(inner, token.src, token.title)

    @staticmethod
    def LinkTokenRender(self, token):
        text = '<span style="color: bule;">[{}]({}&nbsp;"{}")</span>'
        target = escape_url(token.target)
        title = self.RawTextRender(self, token.title)
        inner = self.render_line(token)
        return text.format(inner, target, title)

    @staticmethod
    def AutoLinkTokenRender(self, token):
        text = '<span style="color: bule;">&lt;{}&gt;</span>'
        target = escape_url(token.target)
        return text.format(target)

    @staticmethod
    def HeadTokenRender(self, token):
        text = '<h{level}>{star}&nbsp;{inner}</h{level}><br>'
        inner = self.render_line(token)
        star = '#'*int(token.level)
        return text.format(level=token.level, star=star, inner=inner)

    @staticmethod
    def QuoteTokenRender(self, token):
        text = '<span>&gt;&nbsp;{inner}</span><br>'
        return text.format(inner=self.render_line(token))

    @staticmethod
    def BlockCodeTokenRender(self, token):
        text = '<span>```{attr}\n{inner}\n```</span><br>'
        if token.language:
            attr = 'class={}'.format('lang-{}'.format(token.language))
        else:
            attr = ''
        inner = self.render_line(token)
        return text.format(attr=attr, inner=inner).replace('\n', '<br>')

    @staticmethod
    def SeparatorTokenRender(self, token):
        return '---<br>'

    @staticmethod
    def ListTokenRender(self, token):
        text = '<{tag}{attr}>{inner}</{tag}><br>'
        if token.start:
            tag = 'ol'
            attr = ' start="{}"'.format(token.start)
        else:
            tag = 'ul'
            attr = ''
        inner = self.render_line(token)
        return text.format(tag=tag, attr=attr, inner=inner)

    @staticmethod
    def TableTokenRender(self, token):
        text = '<table>{inner}</table><br>'
        if token.has_header:
            head_text = '<thead>{inner}</thead>'
            header = token.kids[0]
            head_inner = self.TableRowRender(self, header, True)
            head_rendered = head_text.format(inner=head_inner)
        else:
            head_rendered = ''
        body_text = '<tbody>{inner}</tbody>'
        body_inner = self.render_line(token)
        body_rendered = body_text.format(inner=body_inner)
        return text.format(inner=head_rendered + body_rendered)

    @staticmethod
    def RawTextRender(self, token):
        return html.escape(token.content)

    @staticmethod
    def ParagraphTokenRender(self, token):
        return '<span>{}</span><br>'.format(self.render_line(token))

    @staticmethod
    def ListItemRender(self, token):
        return '<li>{}</li>'.format(self.render_line(token))

    @staticmethod
    def TableRowRender(self, token, is_header=False):
        if not is_header and token.header:
            return ""
        text = '<tr>{inner}</tr>'
        inner = ''.join(
            [self.TableCellRender(self, kid, is_header) for kid in token.kids])
        return text.format(inner=inner)

    @staticmethod
    def QuoteItemRender(self, token):
        return '<span>&gt;&nbsp;{}</span><br>'.format(self.render_line(token))

    @staticmethod
    def HTMLBigTokenRender(self, token):
        return html.escape(token.content)

    @staticmethod
    def HTMLLittleTokenRender(self, token):
        return html.escape(token.content)

    @staticmethod
    def TableCellRender(self, token, in_header=False):
        text = '<{tag}{attr}>{inner}</tag>'
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

    @staticmethod
    def DocumentTokenRender(self, token):
        return self.render_line(token)


def escape_url(raw):
    """
    进行url编码
    """
    from urllib.parse import quote
    return quote(raw, safe='/#:')
