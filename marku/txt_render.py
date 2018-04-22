#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
# txt_render.py
__aythor__ = 'Aiyane'
import re
from marku import deal_line

# line
head_pattern = re.compile(r'( *#+)(.*)')
quote_pattern = re.compile(r'( *>+)(.*)')
unorder_list_pattern = re.compile(r'( *)(.*)')
order_list_pattern = re.compile(r'((?: *.*)?\.)(.*)')

# words
strong_pattern = re.compile(r"(\*\*)(.+?)\*\*(?!\*)|(__)(.+)__(?!_)")
emphasis_pattern = re.compile(
    r"(\*)((?:\*\*|[^\*])+?)\*(?!\*)|(_)((?:__|[^_])+?)_")
img_pattern = re.compile(r'\!\[(.*?)\] *\((.+?)(?: *"(.+?)")?\)')
del_pattern = re.compile(r"~~(.+?)~~")
inlinecode_pattern = re.compile(r"`(.+?)`")
link_pattern = re.compile(
    r'\[((?:!\[(?:.+?)\][\[\(](?:.+?)[\)\]])|(?:.+?))\] *\((.+?)(?: *"(.+?)")?\)')
# autolink_pattern = re.compile(r"<([^ ]+?)>")
pattern_list = [strong_pattern, emphasis_pattern, img_pattern,
                del_pattern, inlinecode_pattern, link_pattern]


class Mark(object):
    def __init__(self, content):
        self.func_dict = {strong_pattern: self.strong, emphasis_pattern: self.emphasis, img_pattern: self.img,
                          del_pattern: self.delchar, inlinecode_pattern: self.inlinecode, link_pattern: self.link}

    def paragraph(self, lines):
        # 有换行的段落, 显示为一行
        # 多行
        return deal_line(' '.join(lines), self.func_dict)

    def block_code(self, lines):
        # 多行
        return ''.join(map(lambda x: ''.join(['<p style="color: rgb(149, 204, 94);">', deal_line(x, self.func_dict), '</p>']), lines))

    def tab_code(self, lines):
        # 多行
        return ''.join(map(lambda x: ''.join(['<p style="color: rgb(134, 134, 134);">', deal_line(x, self.func_dict), '</p>']), lines))

    def head(self, line):
        # 一行
        match_obj = head_pattern.match(line)
        tag = match_obj.group(1)
        content = deal_line(match_obj.group(2), self.func_dict)
        level = str(tag.count('#'))
        return ''.join(['<h', level, '>', '<span style="color: rgba(102, 128, 153, 0.4);">', tag,
                        '</span>', '<span style="color: rgb(248, 187, 57);">', content, '</span></h', level, '>'])

    def quote(self, line):
        # 一行
        match_obj = quote_pattern.match(line)
        tag = match_obj.group(1)
        level = str(tag.count('>'))
        tag = tag.replace(">", "&gt;")
        content = deal_line(match_obj.group(2), self.func_dict)
        return ''.join(['<p><span style="color: rgba(139, 158, 177, 0.8);">', tag,
                        '</span><span style="color: rgb(219, 120, 77);">', content, '</span></p>'])

    def underline(self, line):
        # 一行
        return ''.join(['<p style="color: rgba(139, 158, 177, 0.8);">', line, '</p>'])

    def unorder_list(self, line):
        # 一行
        match_obj = unorder_list_pattern.match(line)
        content = deal_line(match_obj.group(2), self.func_dict)
        tag = match_obj.group(1)+content[0]
        return ''.join(['<p><span style="color: rgba(139, 158, 177, 0.8);">', tag, '</span>', content, '</p>'])

    def order_list(self, line):
        # 一行
        match_obj = order_list_pattern.match(line)
        tag = match_obj.group(1)
        content = deal_line(match_obj.group(2), self.func_dict)
        return ''.join(['<p><span style="color: rgba(139, 158, 177, 0.8);">', tag, '</span>', content, '</p>'])

    def strong(self, match_obj):
        # match_obj
        tag, content = [group for group in match_obj.groups()
                        if group is not None]
        return ''.join(['<span style="color: rgba(139, 158, 177, 0.8);">', tag, '</sapn><b style="color: rgb(219, 120, 77);">',
                        deal_line(content, self.func_dict), '</b><span style="color: rgba(139, 158, 177, 0.8);">', tag, '</span>'])

    def emphasis(self, match_obj):
        # match_obj
        tag, content = [group for group in match_obj.groups()
                        if group is not None]
        return ''.join(['<span style="color: rgba(139, 158, 177, 0.8);">', tag, '</span><em>',
                        deal_line(content, self.func_dict), '</em><span style="color: rgba(139, 158, 177, 0.8);">', tag, '</span>'])

    def link(self, match_obj):
        # match_obj
        content = match_obj.group(1)
        target = match_obj.group(2)
        title = match_obj.group(3)
        return ''.join(['<span style="color: rgba(139, 158, 177, 0.8);">[<span style="color: rgb(248, 187, 57);">',
                        deal_line(content, self.func_dict), '</span>](', target, ' ', title, '</span>'])

    def inlinecode(self, word):
        # word
        return ''.join(['<span style="color: rgb(149, 204, 94); background-color: rgba(0, 0, 0, 0.33);">', word, '</span>'])

    def delchar(self, word):
        # word
        return ''.join(['<span style="color: rgba(139, 158, 177, 0.8);">~~</span><del>', deal_line(word[2:-2], self.func_dict),
                        '</del><span style="color: rgba(139, 158, 177, 0.8);">~~</span>'])

    def img(self, word):
        # word
        return ''.join(['<span style="background-color: rgba(0, 0, 0, 0.33);color: rgba(139, 158, 177, 0.8);">', word, '</span>'])

    def deal_lines(self, lines):
        res = []
        buffer = []
        code = False
        tabcode = False

        def init_buffer():
            nonlocal code
            nonlocal tabcode
            if buffer:
                if code:
                    res.append(self.block_code(buffer))
                    code = False
                elif tabcode:
                    res.append(self.tab_code(buffer))
                    tabcode = False
                else:
                    res.append(self.paragraph(buffer))
                buffer.clear()

        for line in lines.split('\n'):
            line = line.replace('\xa0', ' ')
            if code:
                if line == '```':
                    code = False
                    res.append(self.block_code(buffer))
                    buffer.clear()
                else:
                    buffer.append(line)
                continue

            if tabcode:
                if line.startswith(' '*4):
                    buffer.append(line)
                else:
                    res.append(self.tab_code(buffer))
                    tabcode = False
                continue

            if line.strip()[0] == '#':
                init_buffer()
                res.append(self.head(line))
                continue

            if line.strip()[0] == '>':
                init_buffer()
                res.append(self.quote(line))
                continue

            if line.strip()[0] in ('+', '-'):
                init_buffer()
                res.append(self.unorder_list(line))
                continue

            if line.strip().split('.', 1)[0].isdigit():
                init_buffer()
                res.append(self.order_list(line))
                continue

            if line.strip() in ('---', '***', '* * *'):
                init_buffer()
                res.append(self.underline(line))
                continue

            if line.strip().startswith("```"):
                init_buffer()
                buffer.append(line)
                code = True
                continue

            if line.startswith(' '*4):
                init_buffer()
                buffer.append(line)
                tabcode = True

            buffer.append(line)

        init_buffer()
        return ''.join(res)
