#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Marku的简单使用
"""

from marku import Marku
import os
import webbrowser

loc = os.getcwd()
other = """<link rel="stylesheet"
    href="http://cdn.jsdelivr.net/gh/highlightjs/cdn-release@9.12.0/build/styles/default.min.css">
<script src="http://cdn.jsdelivr.net/gh/highlightjs/cdn-release@9.12.0/build/highlight.min.js"></script>
<script >hljs.initHighlightingOnLoad();</script>
"""

md = Marku(loc + "/test2.md", loc + '/style.css', other)
md.render(loc + "/out.html")
webbrowser.open(loc + "/out.html")
