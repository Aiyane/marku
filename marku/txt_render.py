#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
# txt_render.py
__aythor__ = 'Aiyane'
import re

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
escapechar_pattern = re.compile(r"\\([\*\(\)\[\]\~])")
# autolink_pattern = re.compile(r"<([^ ]+?)>")


def init(s):
    s = s.replace("&", "&amp;")
    s = s.replace(" ", "&nbsp;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    s = s.replace('"', "&quot;")
    s = s.replace('\'', "&#x27;")
    return s


class Mark(object):
    def __init__(self):
        self.func_dict = {escapechar_pattern: self.escapechar, strong_pattern: self.strong, emphasis_pattern: self.emphasis, img_pattern: self.img,
                          del_pattern: self.delchar, inlinecode_pattern: self.inlinecode, link_pattern: self.link}

    def paragraph(self, lines):
        # 有换行的段落, 显示为一行
        # 多行
        return ''.join(['<p>', ''.join(map(lambda x: '<line>' + self.deal_line(x) + '</line><br>', lines)), '</p>'])

    def block_code(self, lines):
        # 多行
        return ''.join(map(lambda x: ''.join(['<p style="color: rgb(149, 204, 94);">', x.replace(' ', '&nbsp'), '</p>']), lines))

    def tab_code(self, lines):
        # 多行
        return ''.join(map(lambda x: ''.join(['<p style="color: rgb(134, 134, 134);">', x.replace(' ', '&nbsp'), '</p>']), lines))

    def head(self, line):
        # 一行
        match_obj = head_pattern.match(line)
        tag = match_obj.group(1)
        content = self.deal_line(match_obj.group(2))
        level = str(tag.count('#'))
        return ''.join(['<h', level, '>', '<span style="color: rgba(102, 128, 153, 0.4);">', tag,
                        '</span>', '<span style="color: rgb(248, 187, 57);">', content, '</span></h', level, '>'])

    def table(self, line):
        # 一行
        return ''.join(['<p>', line.replace(' ', '&nbsp'), '</p>'])

    def quote(self, line):
        # 一行
        match_obj = quote_pattern.match(line)
        tag = match_obj.group(1)
        level = str(tag.count('>'))
        tag = tag.replace(">", "&gt;").replace(' ', '&nbsp')
        content = self.deal_line(match_obj.group(2))
        return ''.join(['<p><span style="color: rgba(139, 158, 177, 0.8);">', tag,
                        '</span><span style="color: rgb(219, 120, 77);">', content, '</span></p>'])

    def underline(self, line):
        # 一行
        return ''.join(['<p style="color: rgba(139, 158, 177, 0.8);">', line, '</p>'])

    def unorder_list(self, line):
        # 一行
        match_obj = unorder_list_pattern.match(line)
        content = self.deal_line(match_obj.group(2))
        tag = match_obj.group(1)+content[0]
        return ''.join(['<p><span style="color: rgba(139, 158, 177, 0.8);">', tag.replace(' ', '&nbsp'), '</span>', content[1:], '</p>'])

    def order_list(self, line):
        # 一行
        match_obj = order_list_pattern.match(line)
        tag = match_obj.group(1).replace(' ', '&nbsp')
        content = self.deal_line(match_obj.group(2))
        return ''.join(['<p><span style="color: rgba(139, 158, 177, 0.8);">', tag, '</span>', content, '</p>'])

    def strong(self, match_obj):
        # match_obj
        tag, content = [group for group in match_obj.groups()
                        if group is not None]
        return ''.join(['<span style="color: rgba(139, 158, 177, 0.8);">', tag, '</span><b style="color: rgb(219, 120, 77);">',
                        self.deal_line(content), '</b><span style="color: rgba(139, 158, 177, 0.8);">', tag, '</span>'])

    def emphasis(self, match_obj):
        # match_obj
        tag, content = [group for group in match_obj.groups()
                        if group is not None]
        return ''.join(['<span style="color: rgba(139, 158, 177, 0.8);">', tag, '</span><em>',
                        self.deal_line(content), '</em><span style="color: rgba(139, 158, 177, 0.8);">', tag, '</span>'])

    def link(self, match_obj):
        # match_obj
        content = match_obj.group(1)
        target = match_obj.group(2)
        title = match_obj.group(3)
        return ''.join(['<span style="color: rgba(139, 158, 177, 0.8);">[<span style="color: rgb(248, 187, 57);">',
                        self.deal_line(content), '</span>](', target, ' "', title, '")</span>'])

    def inlinecode(self, match_obj):
        # word
        word = match_obj.group(0)
        return ''.join(['<span style="color: rgb(149, 204, 94); background-color: rgba(0, 0, 0, 0.33);">', word, '</span>'])

    def delchar(self, match_obj):
        # word
        word = match_obj.group(0)
        return ''.join(['<span style="color: rgba(139, 158, 177, 0.8);">~~</span><del>', self.deal_line(word[2:-2]),
                        '</del><span style="color: rgba(139, 158, 177, 0.8);">~~</span>'])

    def img(self, match_obj):
        # word
        word = match_obj.group(0)
        return ''.join(['<span style="background-color: rgba(0, 0, 0, 0.33);color: rgba(139, 158, 177, 0.8);">', word, '</span>'])

    def escapechar(self, match_obj):
        word = match_obj.group(0)
        return init(word)

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
                    buffer.append(line)
                    res.append(self.block_code(buffer))
                    buffer.clear()
                else:
                    buffer.append(line)
                continue

            if tabcode:
                if line.startswith(' '*4):
                    buffer.append(line)
                    continue
                else:
                    res.append(self.tab_code(buffer))
                    buffer.clear()
                    tabcode = False

            if not line.strip():
                init_buffer()
                continue

            if line.strip()[0] == '|' and line.strip()[-1] == '|':
                res.append(self.table(line))
                continue

            if line.strip() in ('---', '***', '* * *'):
                init_buffer()
                res.append(self.underline(line))
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

            if line.strip().startswith("```"):
                init_buffer()
                buffer.append(line)
                code = True
                continue

            if line.startswith(' '*4):
                init_buffer()
                buffer.append(line)
                tabcode = True
                continue

            if line.strip()[0] == '#':
                init_buffer()
                res.append(self.head(line))
                continue

            buffer.append(line)

        init_buffer()
        return ''.join(res)

    def deal_line(self, content):
        res = []
        start = end = 0
        while 1:
            temp_res = None
            minIndex = len(content)
            for pattern in self.func_dict.keys():
                match_obj = pattern.search(content, start)
                if match_obj and start <= match_obj.start() < minIndex:
                    minIndex = match_obj.start()
                    temp_res = self.func_dict[pattern](match_obj)
                    end = match_obj.end()
            # 如果起始位置并不是第一个匹配的位置就在前段生成默认类型
            if start < minIndex:
                res.append(init(content[start:minIndex]))
            if not temp_res:
                break
            # 如果匹配到了就让起始位置改变， 再考察后面的字符
            start = end
            res.append(temp_res)

        return ''.join(res)
