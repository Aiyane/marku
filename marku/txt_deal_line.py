#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
# txt_deal_line.py


def deal_line(content, func_list):
    def init(line):
        s = line.replace("&", "&amp;")
        s = s.replace(" ", "&nbsp;")
        s = s.replace("<", "&lt;")
        s = s.replace(">", "&gt;")
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
        return s
    res = []
    start = end = 0
    while 1:
        close_token = None
        minIndex = len(content)
        for pattern in func_list.keys():
            match_obj = pattern.search(content, start)
            if match_obj and start <= match_obj.start() < minIndex:
                minIndex = match_obj.start()
                close_token = func_list(pattern)
                end = match_obj.end()
        # 如果起始位置并不是第一个匹配的位置就在前段生成默认类型
        if start < minIndex:
            res.append(init(content[start:minIndex]))
        if not close_token:
            break
        # 如果匹配到了就让起始位置改变， 再考察后面的字符
        start = end
        return close_token

    return ''
