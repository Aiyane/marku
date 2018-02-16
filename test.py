#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Marku的简单使用
"""

from marku import Marku
import os
import webbrowser

loc = os.getcwd()

md = Marku(loc + "/test2.md", loc + '/style.css')
md.render(loc + "/out.html")
webbrowser.open(loc + "/out.html")
