#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Aiyane'


def deal_with_line(content, token_types, init_token):
    """处理行内Token
    这里的注释之后写
    """
    index = 0
    close_token = None
    match_obj = None
    end_match = 0
    while index < len(content):
        if_jump = index
		minIndex = len(content)
        for token_type in token_types:
            match_obj = token_type.pattern.search(content, index)
            if match_obj and index < match_obj.start() < minIndex:
                minIndex = match_obj.start()
                close_token = token_type(match_obj)
                end_match = match_obj.end()
            elif match_obj and match_obj.start() == index:
                index = match_obj.end()
                close_token = None
                yield token_type(match_obj)
                break
        if close_token:
            yield init_token(content[index:minIndex])
            yield close_token
            close_token = None
            index = end_match
        elif if_jump == index:
            yield init_token(content[index:])
            index = len(content)
