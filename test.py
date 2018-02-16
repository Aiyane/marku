#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Marku的简单使用
"""

from marku import Marku
import os

loc = os.getcwd()

md = Marku(loc + "/test.md", loc + '/style.css')
md.render(loc + "/out.html")
