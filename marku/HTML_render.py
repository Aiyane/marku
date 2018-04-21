#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__aythor__ = 'Aiyane'
from marku.render import BaseRender
import html
from marku import HTML_token
from itertools import chain


class HTMLRenderer(BaseRender):
    """这是HTML的render, 即渲染各个token成HTML格式"""

    def __init__(self, *extras):
        """构造函数 """
        HTMLToken = self._get_tokens(HTML_token)
        super().__init__(*chain(HTMLToken, extras))

    @staticmethod
    def StrongTokenRender(self, token):
        text = '<strong class="{strongClass}">{}</strong>'
        return text.format(
            self.render_line(token), strongClass=self.tokenClass('strongClass'))

    @staticmethod
    def EmphasisTokenRender(self, token):
        text = '<em class="{emClass}">{}</em>'
        return text.format(
            self.render_line(token), emClass=self.tokenClass('emClass'))

    @staticmethod
    def EscapeCharTokenRender(self, token):
        return self.render_line(token)

    @staticmethod
    def InlineCodeTokenRender(self, token):
        text = '<code class="{codeClass}">{}</code>'
        return text.format(
            self.render_line(token), codeClass=self.tokenClass('codeClass'))

    @staticmethod
    def DeleTokenRender(self, token):
        text = '<del class="{delClass}">{}</del>'
        return text.format(
            self.render_line(token), delClass=self.tokenClass('delClass'))

    @staticmethod
    def ImageTokenRender(self, token):
        text = '<img class="{imgClass}" src={} title={} alt={}>'
        inner = self.render_line(token)
        return text.format(
            token.src, token.title, inner, imgClass=self.tokenClass('imgClass'))

    @staticmethod
    def LinkTokenRender(self, token):
        text = '<a class="{aClass}" href={target} title={title}>{inner}</a>'
        target = escape_url(token.target)
        title = self.RawTextRender(self, token.title)
        inner = self.render_line(token)
        return text.format(
            aClass=self.tokenClass('aClass'), target=target, title=title, inner=inner)

    @staticmethod
    def AutoLinkTokenRender(self, token):
        text = '<a class="{aClass}" href={target}>{inner}</a>'
        target = escape_url(token.target)
        inner = self.render_line(token)
        return text.format(
            aClass=self.tokenClass('aClass'), target=target, inner=inner)

    @staticmethod
    def HeadTokenRender(self, token):
        text = '<h{level} class="{hClass}">{inner}</h{level}>'
        inner = self.render_line(token)
        return text.format(
            hClass=self.tokenClass('hClass'), level=token.level, inner=inner)

    @staticmethod
    def QuoteTokenRender(self, token):
        text = '<blockquote class="{blockquoteClass}">{inner}</blockquote>'
        return text.format(
            blockquoteClass=self.tokenClass('blockquoteClass'),
            inner=self.render_line(token))

    @staticmethod
    def BlockCodeTokenRender(self, token):
        text = '<pre class="{preClass}"><code {attr}>{inner}</code></pre>'
        if token.language:
            attr = 'class="{}"'.format('lang-{}'.format(token.language))
        else:
            attr = ''
        inner = self.render_line(token)
        return text.format(
            preClass=self.tokenClass('preClass'), attr=attr, inner=inner).replace('\n', '<br>')

    @staticmethod
    def SeparatorTokenRender(self, token):
        return '<hr>'

    @staticmethod
    def ListTokenRender(self, token):
        text = '<{tag}{attr}>{inner}</{tag}>'
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
        text = '<table class="{tableClass}">{inner}</table>'
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
        return text.format(
            inner=head_rendered + body_rendered,
            tableClass=self.tokenClass('tableClass'))

    @staticmethod
    def RawTextRender(self, token):
        return html.escape(token.content)

    @staticmethod
    def ParagraphTokenRender(self, token):
        return '<p class="{pClass}">{}</p>'.format(
            self.render_line(token), pClass=self.tokenClass('pClass'))

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
        return '<p>{}</p>'.format(self.render_line(token))

    @staticmethod
    def HTMLBigTokenRender(self, token):
        return token.content

    @staticmethod
    def HTMLLittleTokenRender(self, token):
        return token.content

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
