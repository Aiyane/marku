#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Aiyane'


class BaseRender(object):
    """基础的render类
    如果你要解析成你需要的格式需要有以下规则
    首先你的自定义的render必须继承于BaseRender类
    然后你处理抽象语法树中的Token需要自定义处理函数, 函数的名字必须是
    'Token名'+'Render',例如'ListTokenRender'
    """

    def __init__(self):
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
            'DocumentToken':    self.DocumentTokenRender
        }

    def render(self, token):
        """
        render入口
        """
        return self.render_map[token.__class__.__name__](token)

    def render_line(self, token):
        """
        递归调用子Token
        """
        rendered = [self.render(kid) for kid in token.kids]
        return ''.join(rendered)
