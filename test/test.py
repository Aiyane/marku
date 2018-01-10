#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Aiyane'

import sys
import os

from marku.big_token import DocumentToken
from marku.HTML_render import HTMLRenderer

argv = sys.argv

try:
    with open(argv[1], 'r', encoding='utf-8') as fin:
        AST = DocumentToken(fin)
        rendered = HTMLRenderer().render(AST)
    with open(argv[2], 'w') as f:
        f.write(rendered)
except Exception:
    with open(
            os.path.split(os.path.realpath(__file__))[0] + '/test1.md',
            'r',
            encoding='utf-8') as fin:
        AST = DocumentToken(fin)
        rendered = HTMLRenderer().render(AST)
    with open('output.html', 'w') as f:
        f.write(rendered)
